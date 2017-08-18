from PIL import Image
import numpy as np


def beeps(image,sd,sc):
    if(isinstance(image, str)):
        im = __read(image)
    elif (isinstance(image, np.ndarray)):
        im=image
    else:
        return 0

    if (im.ndim ==3):
        _, _, depth = im.shape
        af=[]
        for i in range(depth):
            im_a = im[..., i]
            im_a = im_a / 255
            af.append(__process(im_a, sd, sc))
        af=np.array([[[r,g,b] for r,g,b in zip(af[0][i],af[1][i],af[2][i]) ]for i in range(af[0].shape[0])])
        af=af*255
        af=af.astype(np.uint8)
        pass
    else:
        im=image/255
        af = __process(im, sd, sc)
        af=af*255
        af=af.astype(np.uint8)
    return af


def __read(path):
    with Image.open(path) as im:
        im = np.array(im)
    return im


def __process(ary, sd, sc):
    sc = 1 - sc;
    c = -0.5 / (sd * sd);
    rho = 1.0 + sc;
    height, width = ary.shape

    # BEEPSHorizontalVertical
    Ihp = ary.copy()
    Ihr = ary.copy()

    Ihp[:, 0] = Ihp[:, 0] / rho;
    for k in range(1, width):
        mu = Ihp[:, k] - rho * Ihp[:, k - 1];
        mu = sc * np.exp(c * mu * mu);
        Ihp[:, k] = mu * Ihp[:, k - 1] + Ihp[:, k] * (1 - mu) / rho;

    Ihr[:, width - 1] = Ihr[:, width - 1] / rho;
    for k in range(width - 2, -1, -1):
        mu = Ihr[:, k] - rho * Ihr[:, k + 1];
        mu = sc * np.exp(c * mu * mu);
        Ihr[:, k] = Ihr[:, k + 1] * mu + Ihr[:, k] * (1 - mu) / rho;

    Ih = Ihp + Ihr - (1 - sc) / rho * ary;

    Ivp = Ih.copy();
    Ivr = Ih.copy();
    Ivp[0, :] = Ivp[0, :] / rho;
    for k in range(1, height):
        mu = Ivp[k, :] - rho * Ivp[k - 1, :];
        mu = sc * np.exp(c * mu * mu);
        Ivp[k, :] = mu * Ivp[k - 1, :] + Ivp[k, :] * (1 - mu) / rho

    Ivr[height-1,:]=Ivr[height-1,:]/ rho;
    for k in range(height-2,-1,-1):
        mu = Ivr[k,:]-rho * Ivr[k + 1,:];
        mu = sc * np.exp(c* mu * mu);
        Ivr[k,:]=Ivp[k + 1,:]*mu + Ivr[k,:]*(1 - mu) / rho;

    IHV = Ivp + Ivr - (1 - sc) / rho * Ih;
    # BEEPSHorizontalVertical end

    # BEEPSVerticalHorizontal
    Vhvp=ary.copy();
    Vhvr=ary.copy();
    Vhvp[0,:]=Vhvp[0,:]/rho;
    for k in range(1,height):
        mu = Vhvp[k,:]-rho * Vhvp[k - 1,:];
        mu = sc* np.exp(c* mu* mu);
        Vhvp[k,:]=mu* Vhvp[k - 1,:]+Vhvp[k,:]*(1 - mu)/ rho;

    Vhvr[height-1,:]=Vhvr[height-1,:]/ rho;
    for k in range(height-2,-1,-1):
        mu = Vhvr[k,:]-rho * Vhvr[k + 1,:];
        mu = sc * np.exp(c* mu* mu);
        Vhvr[k,:]=Vhvr[k + 1,:]*mu + Vhvr[k,:]*(1 - mu) / rho;
    Vhv = Vhvp + Vhvr - (1 - sc) / rho * ary;

    Vhhp = Vhv.copy();
    Vhhr = Vhv.copy();
    Vhhp[:, 0]=Vhhp[:, 0]/ rho;

    for k in range(1,width):
        mu = Vhhp[:, k]-rho * Vhhp[:, k - 1];
        mu = sc * np.exp(c* mu* mu);
        Vhhp[:, k]=mu* Vhhp[:, k - 1]+Vhhp[:, k]*(1 - mu)/ rho;

    Vhhr[:, width-1]=Vhhr[:, width-1]/ rho;
    for k in range(width-2,-1,-1):
        mu = Vhhr[:, k]-rho * Vhhr[:, k + 1];
        mu = sc * np.exp(c* mu * mu);
        Vhhr[:, k]=Vhhr[:, k + 1]*mu + Vhhr[:, k]*(1 - mu)/ rho;
    IVH = Vhhp + Vhhr - (1 - sc) / rho * Vhv;

    return 0.5*(IHV+IVH);