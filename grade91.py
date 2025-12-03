#单位：1/s
#计算认为与19文档相符，注意更改了drivers.py中solvers = [s1,s3,s2]，之前是没有s2的。
#有限元软件调用此库的时候可能也需要有类似的更改，而且driver中实际计算过程可供有限元软件参考
#注意更改drivers.py要改的是实际调用的那个neml，此处可通过命令pip show neml来查找

import sys
sys.path.append('..')

from neml import solvers, interpolate, models, elasticity, drivers, surfaces, hardening, ri_flow,visco_flow, general_flow

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    
  TAlist=[293.15,323.15,348.15,373.15,398.15,423.15,448.15,473.15,498.15,523.15,548.15,573.15,598.15,623.15,648.15,673.15,698.15,723.15,748.15,773.15,798.15,823.15,848.15,873.15,898.15,923.15]
  alpha=[1.05E-05,0.0000108,0.000011,0.0000112,1.14E-05,0.0000116,0.0000118,0.000012,1.22E-05,0.0000124,0.0000125,0.0000127,1.28E-05,0.000013,0.0000131,0.0000133,1.34E-05,0.0000136,0.0000137,0.0000138,0.000014,0.0000142,0.0000144,0.0000146,0.0000149,0.0000152]
  alpha_m = interpolate.PiecewiseLinearInterpolate(list(TAlist), alpha)
  
  E = [213000.0,208000.0,205000.0,201000.0,198000.0,195000.0,191000.0,187000.0,183000.0,179000.0,174000.0,168000.0,161000.0]
  TElist=[293.15,373.15,423.15,473.15,523.15,573.15,623.15,673.15,723.15,773.15,823.15,873.15,923.15]
  E_m = interpolate.PiecewiseLinearInterpolate(list(TElist), E)
  nu = 0.3
  nu_m = interpolate.ConstantInterpolate(nu)
  elastic = elasticity.IsotropicLinearElasticModel(E_m, "youngs", nu_m, "poissons")

  Tlist=[298.15,673.15,773.15,823.15,873.15,923.15]
  h=0.0002
  l=[1.91,1.91,1.71,1.69,1.61,1.51]
  l_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), l)
  surface = surfaces.IsoKinJ2I1(h,l_m)
   
  #注意由温度相关项计算得到的项也是要通过插值得到，但是线性插值的是原参数，而不是计算得到的这些
  A=-9.698
  B=-1.7286
  C=-5.119
  g0=0.3496
  kboltz=1.38068e-29
  b=2.48e-10
  epsilon0=1.0e10
  Tmin = 20+273.15
  Tmax = 650+273.15
  nrate_sens = 40#温度相关参数派生，可能需要更多点数？
  Ts_rate = np.linspace(Tmin, Tmax, num = nrate_sens)
  flow_stress_values = []
  n_values = []
  eta_values = []
  for T in Ts_rate:
    mu = elastic.G(T)
    n_values.append(-mu*b**3.0 / (kboltz * T * A))
    eta_values.append(np.exp(B) * epsilon0 ** (kboltz * T * A / (mu * b**3.0)) * mu)
    flow_stress_values.append(mu * np.exp(C))

  sigma0=interpolate.PiecewiseLinearInterpolate(list(Ts_rate), flow_stress_values)
  n_interp = interpolate.PiecewiseLinearInterpolate(list(Ts_rate), n_values)
  eta_interp = interpolate.PiecewiseLinearInterpolate(list(Ts_rate), eta_values)
  eta_m = visco_flow.ConstantFluidity(eta_interp)
  
  Q=[-96.0,-96.0,-150.0,-151.0,-151.0,-131.0]
  delta=[2.0,1.71,1.71,1.51,1.51,1.0]
  Q_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), Q)
  delta_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), delta)
  iso=hardening.VoceIsotropicHardeningRule(sigma0, Q_m, delta_m)
  iso_vp=hardening.VoceIsotropicHardeningRule(0.0, Q_m, delta_m)
    
  C1=[14500.0,15000.0,19000.0,19200.0,19900.0,19000.0]
  C1_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), C1)
  C2=[12500.0,12500.0,12500.0,12600.0,12400.0,12400.0]
  C2_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), C2)
  gamma1=[141.0,141.0,802.0,792.0,803.0,803.0]
  gamma1_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), gamma1)
  gamma2=[60.6,60.4,200.0,200.0,202.0,202.0]
  gamma2_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), gamma2)
  A1=[1e-15,1e-15,1e-15,1e-15,1e-15,1e-15,1e-15]
  A1_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), A1)
  A2=[1e-15,1e-15,1e-15,1e-15,1e-15,1e-15,1e-15]
  A2_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), A2)
  a1=[3.5,3.5,5.97,5.97,7.47,9.46]
  a1_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), a1)
  a2=[3.5,3.5,5.96,5.96,7.51,9.53]
  a2_m = interpolate.PiecewiseLinearInterpolate(list(Tlist), a2)
  cs=[C1_m,C2_m]
  gamma1_mm=hardening.ConstantGamma(gamma1_m)
  gamma2_mm=hardening.ConstantGamma(gamma2_m)
  gs=[gamma1_mm,gamma2_mm]
  As=[A1_m,A2_m]
  ns=[a1_m,a2_m]
  hmodel = hardening.Chaboche(iso, cs, gs, As, ns)
  hmodel_vp= hardening.Chaboche(iso_vp, cs, gs, As, ns)

  flow = ri_flow.RateIndependentNonAssociativeHardening(surface, hmodel)
  model_pl = models.SmallStrainRateIndependentPlasticity(elastic, flow,alpha=alpha_m)
  
  vmodel = visco_flow.ChabocheFlowRule(surface, hmodel_vp, eta_m,n_interp)
  gflow = general_flow.TVPFlowRule(elastic, vmodel)
  model_vp = models.GeneralIntegrator(elastic, gflow,alpha=alpha_m)
  
  model = models.KMRegimeModel(elastic, [model_pl, model_vp], [g0],
      kboltz, b, epsilon0,alpha=alpha_m)#pl和vp模型都有热膨胀，而km模型也可以加热膨胀，不知道alpha_m应该怎么加
  
  #19文档验证
  strain=np.loadtxt('strain.txt')
  stress=np.loadtxt('stress.txt')
  temperature=np.loadtxt('temperature.txt')
  time=np.loadtxt('time.txt')
  res=drivers.thermomechanical_strain_raw(model, time, temperature, strain,sdir = np.array([1,0,0,0,0,0.0]), verbose = False, substep = 1)
  plt.plot(res['strain'], res['stress'], 'k-')
  plt.plot(strain, stress, 'r-')
  # print(time.size,res['time'].size)
  

  plt.show()
