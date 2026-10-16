"""CSE475 Task 1: real-data EDA. No downloads or synthetic-data fallback."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
from scipy import stats, signal
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px

def locate_root():
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p/'data/manifest.json').exists() and (p/'related_work/papers.json').exists():
            return p
    raise FileNotFoundError('Run from within the CSE475_Task1_Bonn folder.')

def load_inputs(root):
    entries=json.loads((root/'data/manifest.json').read_text())
    meta=json.loads((root/'data/metadata.json').read_text())
    out=root/'outputs/task1'; out.mkdir(parents=True,exist_ok=True)
    if not entries:
        status={'status':'BLOCKED_NO_RAW_EEG','records_analyzed':0,
                'reason':'No authentic raw recordings supplied; no empirical EDA results computed.'}
        (out/'status.json').write_text(json.dumps(status,indent=2))
        return meta, [], pd.DataFrame(), status
    if not meta.get('labels_verified'):
        raise ValueError('Verify label meanings against official documentation first.')
    fs=meta.get('sampling_rate_hz')
    if not isinstance(fs,(int,float)) or not np.isfinite(fs) or fs<=0:
        raise ValueError('Supply a positive documented sampling_rate_hz.')
    definitions=meta.get('class_definitions',{})
    rows=[]; records=[]; paths=set()
    for e in entries:
        for key in ['path','label','source_id']:
            if not e.get(key): raise ValueError(f'Missing {key}: {e}')
        if e['label'] not in definitions:
            raise ValueError(f"Undocumented class: {e['label']}")
        p=(root/'data'/e['path']).resolve()
        if not p.is_relative_to((root/'data').resolve()):
            raise ValueError('Input path must remain within data/.')
        if p in paths: raise ValueError(f'Repeated manifest path: {p}')
        paths.add(p)
        row={**e,'subject_id':e.get('subject_id'),'parse_error':'','n_values':0,
             'nonfinite_count':0,'constant':False,'signal_hash':None}
        try:
            x=np.loadtxt(p,dtype=float,delimiter=e.get('delimiter'),ndmin=1)
            # Accept a single row/column, reject true multi-channel/tabular arrays.
            if x.ndim>1 and min(x.shape)>1:
                raise ValueError('Expected one-channel signal, not a multicolumn feature table.')
            x=x.ravel()
            if len(x)<8: raise ValueError('Fewer than 8 values.')
            row['n_values']=len(x);row['nonfinite_count']=int((~np.isfinite(x)).sum())
            row['constant']=bool(np.isfinite(x).all() and np.ptp(x)==0)
            if np.isfinite(x).all():
                row['signal_hash']=hashlib.sha256(x.astype('<f8').tobytes()).hexdigest()
            records.append((e,x))
        except Exception as exc:
            row['parse_error']=str(exc)
        rows.append(row)
    audit=pd.DataFrame(rows)
    audit['duplicate_signal']=audit.signal_hash.notna() & audit.signal_hash.duplicated(keep=False)
    audit['missing_pct']=100*audit.nonfinite_count/audit.n_values.replace(0,np.nan)
    audit.to_csv(out/'C_raw_quality_audit.csv',index=False)
    counts=audit.groupby('label').size().rename('files').reset_index()
    counts.to_csv(out/'D_manifest_class_counts.csv',index=False)
    status={'status':'RAW_AUDITED','manifest_files':len(audit),
        'parse_failures':int(audit.parse_error.ne('').sum()),
        'nonfinite_values':int(audit.nonfinite_count.sum()),
        'constant_recordings':int(audit.constant.sum()),
        'duplicate_recordings':int(audit.duplicate_signal.sum())}
    (out/'status.json').write_text(json.dumps(status,indent=2))
    return meta, records, audit, status

def split_sources(root,meta,records,audit):
    """Provisional segment allocation for descriptive EDA, NOT subject grouping."""
    from sklearn.model_selection import train_test_split
    if audit.empty: return pd.DataFrame()
    if audit.parse_error.ne('').any() or audit.nonfinite_count.any() or audit.constant.any() or audit.duplicate_signal.any():
        raise ValueError('Resolve quality flags before allocation; see C_raw_quality_audit.csv.')
    m=audit.copy()
    ids=np.arange(len(m))
    dev,reserved=train_test_split(ids,test_size=.4,stratify=m.label,random_state=475)
    val,test=train_test_split(reserved,test_size=.5,stratify=m.iloc[reserved].label,random_state=476)
    m['split']='train';m.loc[val,'split']='validation';m.loc[test,'split']='test'
    m['split_scope']='provisional segment-level only; subject/source independence unknown'
    m[['path','label','subject_id','source_id','split','split_scope']].to_csv(root/'outputs/task1/split_manifest.csv',index=False)
    print('Descriptive EDA uses 300 development segments; reserve 100+100. No model trained.')
    print('Patient and parent-recording IDs unavailable. This is NOT a verified subject/source-independent split.')
    print(pd.crosstab(m.label,m.split))
    return m


def features(x,fs):
    std=float(np.std(x,ddof=1)); dx=np.diff(x)
    v={'mean':np.mean(x),'median':np.median(x),'std':std,'min':np.min(x),'max':np.max(x),
       'q25':np.quantile(x,.25),'q75':np.quantile(x,.75),'skewness':stats.skew(x,bias=False),
       'excess_kurtosis':stats.kurtosis(x,bias=False,fisher=True),'rms':np.sqrt(np.mean(x*x)),
       'peak_to_peak':np.ptp(x),'mean_line_length':np.mean(np.abs(dx)),
       'zero_crossing_rate':np.mean(np.signbit(x[1:])!=np.signbit(x[:-1]))}
    f,p=signal.welch(x,fs=fs,nperseg=min(256,len(x)))
    total=p.sum()
    prob=p/total if total>0 else np.zeros_like(p)
    nz=prob>0
    v['spectral_entropy']=float(-(prob[nz]*np.log2(prob[nz])).sum()/np.log2(len(prob)))
    # Relative discrete PSD-bin mass; denominator includes all returned bins.
    for name,lo,hi in [('delta',.5,4),('theta',4,8),('alpha',8,13),('beta',13,30),('gamma',30,45)]:
        v['relative_'+name]=float(p[(f>=lo)&(f<hi)].sum()/total) if total>0 and fs/2>=hi else np.nan
    return v

def extract_training(root,meta,records,splits):
    if splits.empty:return pd.DataFrame()
    selected=set(splits.loc[splits.split.eq('train'),'path'])
    rows=[]
    for e,x in records:
        if e['path'] in selected: rows.append({'path':e['path'],'label':e['label'],**features(x,meta['sampling_rate_hz'])})
    frame=pd.DataFrame(rows)
    frame.to_csv(root/'outputs/task1/training_features.csv',index=False)
    return frame

def statistics_quality(root,frame):
    if frame.empty:return {}
    out=root/'outputs/task1';x=frame.drop(columns=['path','label'])
    desc=x.describe().T;desc['skewness']=x.skew();desc['excess_kurtosis']=x.kurt()
    desc.to_csv(out/'B_feature_statistics.csv')
    frame.groupby('label').describe().to_csv(out/'B_statistics_by_class.csv')
    q1=x.quantile(.25);q3=x.quantile(.75);iqr=q3-q1
    flags=x.lt(q1-1.5*iqr)|x.gt(q3+1.5*iqr)
    near=x.apply(lambda s:s.value_counts(normalize=True,dropna=False).iloc[0]>=.99)
    quality=pd.DataFrame({'missing_pct':100*x.isna().mean(),'near_constant_99pct':near,'iqr_outliers':flags.sum()})
    quality.to_csv(out/'C_feature_quality.csv')
    flags.to_csv(out/'C_iqr_outlier_flags.csv',index=False)
    corr=x.corr();corr.to_csv(out/'F_correlations.csv')
    pairs=[{'feature_1':a,'feature_2':b,'r':corr.loc[a,b]} for i,a in enumerate(x.columns) for b in x.columns[i+1:] if pd.notna(corr.loc[a,b]) and abs(corr.loc[a,b])>=.95]
    pd.DataFrame(pairs,columns=['feature_1','feature_2','r']).to_csv(out/'F_redundant_pairs.csv',index=False)
    print(quality)
    print('Outliers are review flags, not automatic removal decisions. Correlation is between features, not EEG channels.')
    return {'correlation':corr,'quality':quality,'statistics':desc}

def plots(root,meta,records,splits,frame,summary):
    if frame.empty:return []
    out=root/'outputs/task1';labels=sorted(frame.label.unique());paths=[]
    def save(fig,name):
        p=out/name;fig.savefig(p,dpi=160,bbox_inches='tight');plt.close(fig);paths.append(p)
    counts=frame.label.value_counts().sort_index()
    fig,ax=plt.subplots(figsize=(7,4));counts.plot.bar(ax=ax,color='#1f6f8b');ax.set(title='D | Development class balance',xlabel='Documented class',ylabel='Original files');save(fig,'D_class_balance.png')
    fig,axs=plt.subplots(len(labels),1,figsize=(10,2.2*len(labels)),squeeze=False)
    train=set(frame.path)
    for ax,label in zip(axs[:,0],labels):
        e,x=next((e,x) for e,x in records if e['path'] in train and e['label']==label)
        ax.plot(np.arange(len(x))/meta['sampling_rate_hz'],x,lw=.6);ax.set(title=f"Development example: {label} | {e['path']}",xlabel='Seconds',ylabel='Raw amplitude')
    fig.tight_layout();save(fig,'E_signal_examples.png')
    chosen=['std','rms','mean_line_length','spectral_entropy']
    fig,axs=plt.subplots(2,2,figsize=(10,7))
    for ax,col in zip(axs.ravel(),chosen):
        for label in labels:ax.hist(frame.loc[frame.label.eq(label),col].dropna(),bins=15,alpha=.45,label=label)
        ax.set(title=col,xlabel='Feature value',ylabel='Files');ax.legend(fontsize=7)
    fig.tight_layout();save(fig,'E_histograms.png')
    for kind in ['box','violin']:
        fig,axs=plt.subplots(2,2,figsize=(10,7))
        for ax,col in zip(axs.ravel(),chosen):
            values=[frame.loc[frame.label.eq(label),col].dropna().to_numpy() for label in labels]
            if kind=='box':ax.boxplot(values,tick_labels=labels)
            else:
                for i,v in enumerate(values,1):
                    if len(v)>1 and np.ptp(v)>0:ax.violinplot([v],positions=[i],showmedians=True)
                ax.set_xticks(range(1,len(labels)+1),labels)
            ax.set(title=col,xlabel='Class',ylabel='Feature value')
        fig.tight_layout();save(fig,f'E_{kind}plots.png')
    corr=summary['correlation'];fig,ax=plt.subplots(figsize=(11,9));im=ax.imshow(corr,vmin=-1,vmax=1,cmap='coolwarm');ax.set_xticks(range(len(corr)),corr.columns,rotation=90,fontsize=7);ax.set_yticks(range(len(corr)),corr.index,fontsize=7);ax.set_title('F | Development feature correlations');fig.colorbar(im,ax=ax);fig.tight_layout();save(fig,'F_heatmap.png')
    x=frame.drop(columns=['path','label']);usable=x.columns[x.notna().all() & x.std().gt(1e-12)]
    if len(usable)<2:raise ValueError('Not enough complete varying training features for PCA.')
    z=StandardScaler().fit_transform(x[usable]);pca=PCA(n_components=min(3,len(usable),len(x))).fit(z);coord=pca.transform(z)
    pc=pd.DataFrame(coord,columns=[f'PC{i+1}' for i in range(coord.shape[1])]);pc['label']=frame.label.to_numpy();pc['path']=frame.path.to_numpy();pc.to_csv(out/'G_pca_coordinates.csv',index=False)
    (out/'G_pca_metadata.json').write_text(json.dumps({'features':list(usable),'explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'scope':'development only'},indent=2))
    fig,ax=plt.subplots(figsize=(7,5))
    for label in labels:
        mask=pc.label.eq(label);ax.scatter(pc.loc[mask,'PC1'],pc.loc[mask,'PC2'],s=20,alpha=.7,label=label)
    ax.set(title='G | Development-only PCA (descriptive, not accuracy)',xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.1%})');ax.legend();save(fig,'G_pca_2d.png')
    for fig,name in [(px.scatter(pc,x='PC1',y='PC2',color='label',hover_data=['path'],title='H | Development PCA: hover for file ID'),'H_pca_interactive.html'),(px.box(frame,x='label',y='rms',points='all',hover_data=['path'],title='H | RMS distribution: inspect overlap and outliers'),'H_rms_interactive.html')]:
        fig.write_html(out/name,include_plotlyjs=True,full_html=True);paths.append(out/name)
    if 'PC3' in pc:
        px.scatter_3d(pc,x='PC1',y='PC2',z='PC3',color='label',hover_data=['path'],title='H | Development-only 3D PCA').write_html(out/'H_pca_3d.html',include_plotlyjs=True)
    readings=[f'Development files analyzed: {len(frame)}; class counts: {counts.to_dict()}.',
        'Class balance: use macro-F1 and class recall; observed counts describe this training partition only.',
        f"Near-constant features: {summary['quality'].index[summary['quality'].near_constant_99pct].tolist()}. Review before selecting features; fit any selector on development only.",
        f"Feature outlier flags: {int(summary['quality'].iqr_outliers.sum())}. Inspect original traces; do not remove seizure-related extremes automatically.",
        f'First two PCs explain {pca.explained_variance_ratio_[:2].sum():.1%} of standardized training variance. Visual separation is not evidence of held-out predictive performance.',
        'Review histograms/boxplots/violins for overlap before stating which classes separate; inspect interactive point IDs to trace unusual records.',
        'Frequency bands above Nyquist are marked missing, not invented. Unavailable features are excluded from PCA and listed in its metadata.']
    (out/'interpretation_notes.txt').write_text('\n\n'.join(readings))
    print('\n\n'.join(readings))
    return paths
