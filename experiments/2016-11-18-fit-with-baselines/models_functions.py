import numpy as np

def mf_noseg(T, alpha, ONEoverN, ba_init, bi_init, pv, omega):
    
    # Network size
    N=1./ONEoverN
    
    # Initial conditions
    pBI0, pBA0, pFI0, pFA0, pS0 = N*bi_init, N*ba_init, 0., 0., N*(1.-ba_init-bi_init)
    
    ba = []
    fa = []
    for i in T:
        
        ba.append(pBA0)
        fa.append(pFA0)
        
        f = pBA0/N
        pBI1 = alpha * f * pS0 + omega * pBA0 + (1. - pv) * (1 - f) * pBI0
        pBA1 = (1. - pv) * f  * pBI0 + (1. - omega) * (1. - pv) * pBA0
        pFI1 = (1-alpha) * f * pS0 + omega * pFA0 + pv * (pBI0 + (1. - omega) * pBA0) + (1 - f) * pFI0
        pFA1 = f * pFI0 + (1. - omega) * pFA0
        pS1 = (1 - f) * pS0
        
        #update
        pBI0, pBA0, pFI0, pFA0, pS0 = pBI1, pBA1, pFI1, pFA1, pS1
        
        if float(pBI0)<=0.0000000001:
            pBI0=0.0
        if float(pBA0)<=0.0000000001:
            pBA0=0.0
        if float(pFI0)<=0.0000000001:
            pFI0=0.0
        if float(pFA0)<=0.0000000001:
            pFA0=0.0
        if float(pS0)<=0.0000000001:
            pS0=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))

# To return only one of the types (needed for fitting only against one type)
def mf_noseg_BA(T, alpha, ONEoverN, ba_init, bi_init, pv, omega):
    return mf_noseg(T, alpha, ONEoverN, ba_init, bi_init, pv, omega)[0]

def mf_noseg_FA(T, alpha, ONEoverN, ba_init, bi_init, pv, omega):
    return mf_noseg(T, alpha, ONEoverN, ba_init, bi_init, pv, omega)[1]


def mf_noseg_FI(T, alpha, ONEoverN, ba_init, bi_init, fa_init, fi_init, pv, omega):
    
    # Network size
    N=1./ONEoverN
    
    # Initial conditions
    pBI0, pBA0, pFI0, pFA0, pS0 = N*bi_init, N*ba_init, N*fi_init, N*fa_init, N*(1.-ba_init-bi_init-fa_init-fi_init)
    
    ba = []
    fa = []
    for i in T:
        
        ba.append(pBA0)
        fa.append(pFA0)
        
        f = pBA0/N
        pBI1 = alpha * f * pS0 + omega * pBA0 + (1. - pv) * (1 - f) * pBI0
        pBA1 = (1. - pv) * f  * pBI0 + (1. - omega) * (1. - pv) * pBA0
        pFI1 = (1-alpha) * f * pS0 + omega * pFA0 + pv * (pBI0 + (1. - omega) * pBA0) + (1 - f) * pFI0
        pFA1 = f * pFI0 + (1. - omega) * pFA0
        pS1 = (1 - f) * pS0
        
        #update
        pBI0, pBA0, pFI0, pFA0, pS0 = pBI1, pBA1, pFI1, pFA1, pS1
        
        if float(pBI0)<=0.0000000001:
            pBI0=0.0
        if float(pBA0)<=0.0000000001:
            pBA0=0.0
        if float(pFI0)<=0.0000000001:
            pFI0=0.0
        if float(pFA0)<=0.0000000001:
            pFA0=0.0
        if float(pS0)<=0.0000000001:
            pS0=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))

# To return only one of the types (needed for fitting only against one type)
def mf_noseg_FI_BA(T, alpha, ONEoverN, ba_init, bi_init, fa_init, fi_init, pv, omega):
    return mf_noseg_FI(T, alpha, ONEoverN, ba_init, bi_init, fa_init, fi_init, pv, omega)[0]

def mf_noseg_FI_FA(T, alpha, ONEoverN, ba_init, bi_init, fa_init, fi_init, pv, omega):
    return mf_noseg_FI(T, alpha, ONEoverN, ba_init, bi_init, fa_init, fi_init, pv, omega)[1]


def mf_seg(T, alphag, alphas, ONEoverN, ba_initg, bi_initg, ba_inits, bi_inits, pvg, pvs, omega, gulsize, s):
    
    # Network and component sizes
    N=1./ONEoverN
    N_gullible=N*gulsize
    N_skeptic=N-N_gullible
    
    
    # Initial conditions
    # Gullible
    pBI0g, pBA0g, pFI0g, pFA0g, pS0g = N_gullible*bi_initg, N_gullible*ba_initg, 0.0, 0.0, N_gullible*(1.- (ba_initg+bi_initg))
    # Skeptical
    pBI0s, pBA0s, pFI0s, pFA0s, pS0s = N_skeptic*bi_inits, N_skeptic*ba_inits, 0.0, 0.0, N_skeptic*(1.- (ba_inits+bi_inits))
    
    ba=[]
    fa=[]
    
    for i in T:
        
        # record
        ba.append(pBA0g+pBA0s)
        fa.append(pFA0g+pFA0s)
        
        # update
        fg  = s*pBA0g/N_gullible+(1-s)*pBA0s/N_skeptic
        fs = s*pBA0s/N_skeptic+(1-s)*pBA0g/N_gullible
        
        pBI1g = alphag * fg * pS0g + omega * pBA0g + (1. - pvg) * (1. - fg) * pBI0g
        pBA1g = (1. - pvg) * fg * pBI0g + (1. - omega) * (1. - pvg) * pBA0g
        pFI1g = (1-alphag) * fg * pS0g + omega * pFA0g + pvg * (pBI0g + (1. - omega) * pBA0g) + (1 - fg) * pFI0g
        pFA1g = fg * pFI0g + (1. - omega) * pFA0g
        pS1g = (1. - fg) * pS0g
        
        pBI1s = alphas * fs * pS0s + omega * pBA0s + (1. - pvs) * (1. - fs) * pBI0s
        pBA1s = (1. - pvs) * fs * pBI0s + (1. - omega) * (1. - pvs) * pBA0s
        pFI1s = (1-alphas) * fs * pS0s + omega * pFA0s + pvs * (pBI0s + (1. - omega) * pBA0s) + (1 - fs) * pFI0s
        pFA1s = fs * pFI0s + (1. - omega) * pFA0s
        pS1s = (1. - fs) * pS0s
        
        pBI0g, pBA0g, pFI0g, pFA0g, pS0g = pBI1g, pBA1g, pFI1g, pFA1g, pS1g
        pBI0s, pBA0s, pFI0s, pFA0s, pS0s = pBI1s, pBA1s, pFI1s, pFA1s, pS1s
        
        if float(pBI0s)<=0.0000000001:
            pBI0s=0.0
        if float(pBA0s)<=0.0000000001:
            pBA0s=0.0
        if float(pFI0s)<=0.0000000001:
            pFI0s=0.0
        if float(pFA0s)<=0.0000000001:
            pFA0s=0.0
        if float(pS0s)<=0.0000000001:
            pS0s=0.0
        if float(pBI0g)<=0.0000000001:
            pBI0g=0.0
        if float(pBA0g)<=0.0000000001:
            pBA0g=0.0
        if float(pFI0g)<=0.0000000001:
            pFI0g=0.0
        if float(pFA0g)<=0.0000000001:
            pFA0g=0.0
        if float(pS0g)<=0.0000000001:
            pS0g=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))


def mf_seg_FI(T, alphag, alphas, ONEoverN, ba_initg, bi_initg, ba_inits, bi_inits,
              fa_initg, fi_initg, fa_inits, fi_inits, pvg, pvs, omega, gulsize, s):
    
    # Network and component sizes
    N=1./ONEoverN
    N_gullible=N*gulsize
    N_skeptic=N-N_gullible
    
    
    # Initial conditions
    # Gullible
    pBI0g, pBA0g, pFI0g, pFA0g, pS0g = N_gullible*bi_initg, N_gullible*ba_initg, N_gullible*fi_initg, N_gullible*fa_initg, N_gullible*(1.- (ba_initg+bi_initg+fa_initg+fi_initg))
    # Skeptical
    pBI0s, pBA0s, pFI0s, pFA0s, pS0s = N_skeptic*bi_inits, N_skeptic*ba_inits, N_skeptic*fi_inits, N_skeptic*fa_inits, N_skeptic*(1.- (ba_inits+bi_inits+fa_inits+fi_inits))
    
    ba=[]
    fa=[]
    
    for i in T:
        
        # record
        ba.append(pBA0g+pBA0s)
        fa.append(pFA0g+pFA0s)
        
        # update
        fg  = s*pBA0g/N_gullible+(1-s)*pBA0s/N_skeptic
        fs = s*pBA0s/N_skeptic+(1-s)*pBA0g/N_gullible
        
        pBI1g = alphag * fg * pS0g + omega * pBA0g + (1. - pvg) * (1. - fg) * pBI0g
        pBA1g = (1. - pvg) * fg * pBI0g + (1. - omega) * (1. - pvg) * pBA0g
        pFI1g = (1-alphag) * fg * pS0g + omega * pFA0g + pvg * (pBI0g + (1. - omega) * pBA0g) + (1 - fg) * pFI0g
        pFA1g = fg * pFI0g + (1. - omega) * pFA0g
        pS1g = (1. - fg) * pS0g
        
        pBI1s = alphas * fs * pS0s + omega * pBA0s + (1. - pvs) * (1. - fs) * pBI0s
        pBA1s = (1. - pvs) * fs * pBI0s + (1. - omega) * (1. - pvs) * pBA0s
        pFI1s = (1-alphas) * fs * pS0s + omega * pFA0s + pvs * (pBI0s + (1. - omega) * pBA0s) + (1 - fs) * pFI0s
        pFA1s = fs * pFI0s + (1. - omega) * pFA0s
        pS1s = (1. - fs) * pS0s
        
        pBI0g, pBA0g, pFI0g, pFA0g, pS0g = pBI1g, pBA1g, pFI1g, pFA1g, pS1g
        pBI0s, pBA0s, pFI0s, pFA0s, pS0s = pBI1s, pBA1s, pFI1s, pFA1s, pS1s
        
        if float(pBI0s)<=0.0000000001:
            pBI0s=0.0
        if float(pBA0s)<=0.0000000001:
            pBA0s=0.0
        if float(pFI0s)<=0.0000000001:
            pFI0s=0.0
        if float(pFA0s)<=0.0000000001:
            pFA0s=0.0
        if float(pS0s)<=0.0000000001:
            pS0s=0.0
        if float(pBI0g)<=0.0000000001:
            pBI0g=0.0
        if float(pBA0g)<=0.0000000001:
            pBA0g=0.0
        if float(pFI0g)<=0.0000000001:
            pFI0g=0.0
        if float(pFA0g)<=0.0000000001:
            pFA0g=0.0
        if float(pS0g)<=0.0000000001:
            pS0g=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))


def mf_seg_orig(T, alpha, ONEoverN, ba_initg, bi_initg, ba_inits, bi_inits, pvs, omega, gulsize, s):
    
    # Network and component sizes
    N=1./ONEoverN
    N_gullible=N*gulsize
    N_skeptic=N-N_gullible
    
    #parameters
    pvg = 0
    alphag = alpha
    alphas = alpha
    
    # Initial conditions
    # Gullible
    pBI0g, pBA0g, pFI0g, pFA0g, pS0g = N_gullible*bi_initg, N_gullible*ba_initg, 0.0, 0.0, N_gullible*(1.- (ba_initg+bi_initg))
    # Skeptical
    pBI0s, pBA0s, pFI0s, pFA0s, pS0s = N_skeptic*bi_inits, N_skeptic*ba_inits, 0.0, 0.0, N_skeptic*(1.- (ba_inits+bi_inits))
    
    ba=[]
    fa=[]
    
    for i in T:
        
        # record
        ba.append(pBA0g+pBA0s)
        fa.append(pFA0g+pFA0s)
        
        # update
        fg  = s*pBA0g/N_gullible+(1-s)*pBA0s/N_skeptic
        fs = s*pBA0s/N_skeptic+(1-s)*pBA0g/N_gullible
        
        pBI1g = alphag * fg * pS0g + omega * pBA0g + (1. - pvg) * (1. - fg) * pBI0g
        pBA1g = (1. - pvg) * fg * pBI0g + (1. - omega) * (1. - pvg) * pBA0g
        pFI1g = (1-alphag) * fg * pS0g + omega * pFA0g + pvg * (pBI0g + (1. - omega) * pBA0g) + (1 - fg) * pFI0g
        pFA1g = fg * pFI0g + (1. - omega) * pFA0g
        pS1g = (1. - fg) * pS0g
        
        pBI1s = alphas * fs * pS0s + omega * pBA0s + (1. - pvs) * (1. - fs) * pBI0s
        pBA1s = (1. - pvs) * fs * pBI0s + (1. - omega) * (1. - pvs) * pBA0s
        pFI1s = (1-alphas) * fs * pS0s + omega * pFA0s + pvs * (pBI0s + (1. - omega) * pBA0s) + (1 - fs) * pFI0s
        pFA1s = fs * pFI0s + (1. - omega) * pFA0s
        pS1s = (1. - fs) * pS0s
        
        pBI0g, pBA0g, pFI0g, pFA0g, pS0g = pBI1g, pBA1g, pFI1g, pFA1g, pS1g
        pBI0s, pBA0s, pFI0s, pFA0s, pS0s = pBI1s, pBA1s, pFI1s, pFA1s, pS1s
        
        if float(pBI0s)<=0.0000000001:
            pBI0s=0.0
        if float(pBA0s)<=0.0000000001:
            pBA0s=0.0
        if float(pFI0s)<=0.0000000001:
            pFI0s=0.0
        if float(pFA0s)<=0.0000000001:
            pFA0s=0.0
        if float(pS0s)<=0.0000000001:
            pS0s=0.0
        if float(pBI0g)<=0.0000000001:
            pBI0g=0.0
        if float(pBA0g)<=0.0000000001:
            pBA0g=0.0
        if float(pFI0g)<=0.0000000001:
            pFI0g=0.0
        if float(pFA0g)<=0.0000000001:
            pFA0g=0.0
        if float(pS0g)<=0.0000000001:
            pS0g=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))


def mf_seg_orig_FI(T, alpha, ONEoverN, ba_initg, bi_initg, ba_inits, bi_inits,
                   fa_initg, fi_initg, fa_inits, fi_inits, pvs, omega, gulsize, s):
    
    # Network and component sizes
    N=1./ONEoverN
    N_gullible=N*gulsize
    N_skeptic=N-N_gullible
    
    #parameters
    pvg = 0
    alphag = alpha
    alphas = alpha
    
    # Initial conditions
    # Gullible
    pBI0g, pBA0g, pFI0g, pFA0g, pS0g = N_gullible*bi_initg, N_gullible*ba_initg, N_gullible*fi_initg, N_gullible*fa_initg, N_gullible*(1.- (ba_initg+bi_initg+fa_initg+fi_initg))
    # Skeptical
    pBI0s, pBA0s, pFI0s, pFA0s, pS0s = N_skeptic*bi_inits, N_skeptic*ba_inits, N_skeptic*fi_inits, N_skeptic*fa_inits, N_skeptic*(1.- (ba_inits+bi_inits+fa_inits+fi_inits))
    
    ba=[]
    fa=[]
    
    for i in T:
        
        # record
        ba.append(pBA0g+pBA0s)
        fa.append(pFA0g+pFA0s)
        
        # update
        fg  = s*pBA0g/N_gullible+(1-s)*pBA0s/N_skeptic
        fs = s*pBA0s/N_skeptic+(1-s)*pBA0g/N_gullible
        
        pBI1g = alphag * fg * pS0g + omega * pBA0g + (1. - pvg) * (1. - fg) * pBI0g
        pBA1g = (1. - pvg) * fg * pBI0g + (1. - omega) * (1. - pvg) * pBA0g
        pFI1g = (1-alphag) * fg * pS0g + omega * pFA0g + pvg * (pBI0g + (1. - omega) * pBA0g) + (1 - fg) * pFI0g
        pFA1g = fg * pFI0g + (1. - omega) * pFA0g
        pS1g = (1. - fg) * pS0g
        
        pBI1s = alphas * fs * pS0s + omega * pBA0s + (1. - pvs) * (1. - fs) * pBI0s
        pBA1s = (1. - pvs) * fs * pBI0s + (1. - omega) * (1. - pvs) * pBA0s
        pFI1s = (1-alphas) * fs * pS0s + omega * pFA0s + pvs * (pBI0s + (1. - omega) * pBA0s) + (1 - fs) * pFI0s
        pFA1s = fs * pFI0s + (1. - omega) * pFA0s
        pS1s = (1. - fs) * pS0s
        
        pBI0g, pBA0g, pFI0g, pFA0g, pS0g = pBI1g, pBA1g, pFI1g, pFA1g, pS1g
        pBI0s, pBA0s, pFI0s, pFA0s, pS0s = pBI1s, pBA1s, pFI1s, pFA1s, pS1s
        
        if float(pBI0s)<=0.0000000001:
            pBI0s=0.0
        if float(pBA0s)<=0.0000000001:
            pBA0s=0.0
        if float(pFI0s)<=0.0000000001:
            pFI0s=0.0
        if float(pFA0s)<=0.0000000001:
            pFA0s=0.0
        if float(pS0s)<=0.0000000001:
            pS0s=0.0
        if float(pBI0g)<=0.0000000001:
            pBI0g=0.0
        if float(pBA0g)<=0.0000000001:
            pBA0g=0.0
        if float(pFI0g)<=0.0000000001:
            pFI0g=0.0
        if float(pFA0g)<=0.0000000001:
            pFA0g=0.0
        if float(pS0g)<=0.0000000001:
            pS0g=0.0
    
    return np.cumsum(np.asarray(ba)), np.cumsum(np.asarray(fa))

#UNIFYING MODEL (Moreno et al., 2016)
def sir_unified(T,  beta, alpha, delta1, delta2, gamma, eta, lamda, ONEoverN, X_init, Y_init, Z_init):
    # Network and component sizes
    N = 1. / ONEoverN
    
    X=[]
    Y=[]
    Z=[]
    
    for i in T:
        
        #record
        X.append(X0)
        Y.append(Y0)
        Z.append(Z0)
        
        #update
        a = exp(-lamda * (1 - delta1 - delta2) * Y0)
        b = 1 - alpha * (Y0 + Z0)
        c = 1 - beta * X0

        X1 = Y0 * delta1 + Z0 * gamma
        Y1 = X0 * eta + Z0 * (1 - gamma)
        Z1 = X0 * (1 - eta) + Y0 * (1 - delta1)
        
        X0, Y0, Z0 = X1, Y1, Z1

        if float(X0) <= 0.0000000001:
            X0 = 0.0
        if float(Y0) <= 0.0000000001:
            Y0 = 0.0
        if float(Z0) <= 0.0000000001:
            Z0 = 0.0
            
    return np.cumsum(np.asarray(X)), np.cumsum(np.asarray(Y)), np.cumsum(np.asarray(Z)) 



