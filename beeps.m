function x=beeps(ary,sc,sd)

	sc = 1 - sc;
    c = -0.5 / (sd * sd);
    rho = 1.0 + sc;
    height, width = size(ary)

    # BEEPSHorizontalVertical
    Ihp = ary
    Ihr = ary

    Ihp(:, 1) = Ihp(:, 1) / rho;
    for k =2:width:
        mu = Ihp(:, k) - rho * Ihp(:, k - 1);
        mu = sc * np.exp(c * mu * mu);
        Ihp(:, k) = mu * Ihp(:, k - 1) + Ihp(:, k) * (1 - mu) / rho;
	end
    Ihr(:, width ) = Ihr(:, width ) / rho;
	for k=width-1:-1:1
        mu = Ihr(:, k) - rho * Ihr(:, k + 1);
        mu = sc * np.exp(c * mu * mu);
        Ihr(:, k) = Ihr(:, k + 1) * mu + Ihr(:, k) * (1 - mu) / rho;
	end

    Ih = Ihp + Ihr - (1 - sc) / rho * ary;


    Ivp = Ih;
    Ivr = Ih;
    Ivp(1, :) = Ivp(1, :) / rho;
	for k=2:height
        mu = Ivp(k, :) - rho * Ivp(k - 1, :);
        mu = sc * np.exp(c * mu * mu);
        Ivp(k, :) = mu * Ivp(k - 1, :) + Ivp(k, :) * (1 - mu) / rho
	end
    Ivr(height,:)=Ivr(height,:)/ rho;
 %  for k in range(height-2,-1,-1):
	for k=height-1:-1:1
        mu = Ivr(k,:)-rho * Ivr(k + 1,:);
        mu = sc * np.exp(c* mu * mu);
        Ivr(k,:)=Ivp(k + 1,:)*mu + Ivr(k,:)*(1 - mu) / rho;
	end
    IHV = Ivp + Ivr - (1 - sc) / rho * Ih;
    # BEEPSHorizontalVertical end

    # BEEPSVerticalHorizontal
    Vhvp=ary;
    Vhvr=ary;
    Vhvp(1,:)=Vhvp(1,:)/rho;
   % for k in range(1,height):
	for k=2:height:
        mu = Vhvp(k,:)-rho * Vhvp(k - 1,:);
        mu = sc* np.exp(c* mu* mu);
        Vhvp(k,:)=mu* Vhvp(k - 1,:)+Vhvp(k,:)*(1 - mu)/ rho;
	end
	
    Vhvr(height,:)=Vhvr(height,:)/ rho;
%    for k in range(height-2,-1,-1):
	for k=height-1:-1:1
        mu = Vhvr(k,:)-rho * Vhvr(k + 1,:);
        mu = sc * np.exp(c* mu* mu);
        Vhvr(k,:)=Vhvr(k + 1,:)*mu + Vhvr(k,:)*(1 - mu) / rho;
	end
    Vhv = Vhvp + Vhvr - (1 - sc) / rho * ary;

    Vhhp = Vhv;
    Vhhr = Vhv;
	
    Vhhp(:, 1)=Vhhp(:, 1)/ rho;
  %  for k in range(1,width):
	for k=2:width
        mu = Vhhp(:, k)-rho * Vhhp(:, k - 1);
        mu = sc * np.exp(c* mu* mu);
        Vhhp(:, k)=mu* Vhhp(:, k - 1)+Vhhp(:, k)*(1 - mu)/ rho;
	end
    Vhhr(:, width)=Vhhr(:, width)/ rho;
 %   for k in range(width-2,-1,-1):
	for k=width-1:-1:1
        mu = Vhhr(:, k)-rho * Vhhr(:, k + 1);
        mu = sc * np.exp(c* mu * mu);
        Vhhr(:, k)=Vhhr(:, k + 1)*mu + Vhhr(:, k)*(1 - mu)/ rho;
	end 
    IVH = Vhhp + Vhhr - (1 - sc) / rho * Vhv;

    x=0.5*(IHV+IVH);

end
