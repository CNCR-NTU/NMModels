-- Libraries used --

Library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use IEEE.std_logic_unsigned.all;
use ieee.fixed_float_types.all;
--!ieee_proposed for fixed point
use ieee.fixed_pkg.all;
--!ieee_proposed for floating point
use ieee.float_pkg.all;

entity HH is

generic 
	(
		DATA_WIDTH : natural := 56;
		ADDR_WIDTH : natural := 32
	);

port (clk		: IN std_logic;
		reset		: IN std_logic;
		data_ready: IN std_logic;
		result	: IN	STD_LOGIC_VECTOR (7 downto 0);
		exp_res1	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res2	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res3	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res4	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res5	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res6	: IN	STD_LOGIC_VECTOR (31 downto 0);
		waddr		: OUT std_logic_vector((ADDR_WIDTH-1) downto 0);
		data		: OUT std_logic_vector((DATA_WIDTH-1) downto 0);
		we			: OUT std_logic;
		queue		: out std_logic_vector((ADDR_WIDTH-1) downto 0);
		rst		: OUT std_logic;
		exp_data1	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data2	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data3	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data4	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data5	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data6	: out	STD_LOGIC_VECTOR (31 downto 0);
		debug		: OUT std_logic_vector (7 downto 0)
		);
end HH;

-- architecture body --
architecture HH_arch of HH is
constant	expDelay:		natural									:=17;
signal	qAux:					std_logic_vector((ADDR_WIDTH-1) downto 0):=(others =>'0');
signal	ct:					natural							:=0;
signal	count:					natural							:=0;
signal	rst_flag: 				std_logic						:='0';
signal	conf_flag:				std_logic						:='0';
signal	cycles:					std_logic_vector (15 downto 0)   :=(others=>'0');
signal	timestamp:				natural							:=0;
signal	rk_flag:				std_logic						:='0';
signal	k1:					float32;
signal 	m1:					float32;
signal	n1:					float32;
signal	h1:					float32;
signal	qk:					float32;
signal	qm:					float32;
signal	qn:					float32;
signal	qh:					float32;
signal	k2:					float32;
signal	m2:					float32;
signal	n2:					float32;
signal	h2:					float32;
signal	dt:					float32;
signal 	countRK:				natural							:=0;
signal 	ENa:					float32;
signal	EK: 					float32;
signal	El:					float32;
signal 	gbarNa:				float32;
signal	gbarK:				float32;
signal 	gbarl:				float32;
signal 	gNa:					float32;
signal	gK:					float32;
signal 	gl:					float32;
signal	Vm:					float32;
signal	Cm:					float32;	
signal 	aV:					float32;
signal 	aV_1:					float32;
signal 	aV_2:					float32;
signal 	aux:					std_logic_vector (31 downto 0)   :=(others=>'0');
signal 	h:					float32;
signal 	m:					float32;
signal 	n:					float32;
signal 	IK:				float32;
signal 	INa:				float32;
signal 	Il:				float32;
signal 	I:					float32;
signal	aux1:				float32;
signal	aux2:				float32;
signal	aux3:				float32;
signal	aux4:				float32;
signal	aux5:				float32;
signal	aux6:				float32;
signal	aux7:				float32;
signal	aux8:				float32;
signal	aux9:				float32;
signal	aux10:			float32;
signal	aux11:			float32;
signal	aux12:			float32;
signal	time_step:		float32;
signal	compute_flag:	std_logic 								:='0';
signal	exp_flag:		std_logic 								:='0';
signal	spike:			std_logic 								:='0';
		--- process ---
BEGIN
	process(clk, reset, rk_flag, Av, qk, spike)
	variable ct1: natural :=0;
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			conf_flag<='0';
			ct<=0;
			count<=0;
			rst_flag<='0';
			cycles<=(others =>'0');
			timestamp<=0;
			we<='0';
			data<=(others => '0');
			waddr<=(others => '0');
			queue<=(others => '0');
			time_step<=to_float(0.0,time_step);
			compute_flag<='0';
			aux<=(others=>'0');
			exp_data1<=(others=>'0');
			exp_data2<=(others=>'0');
			exp_data3<=(others=>'0');
			exp_data4<=(others=>'0');
			exp_data5<=(others=>'0');
			exp_data6<=(others=>'0');
			aux1<=to_float(0.0,aux1);
			aux2<=to_float(0.0,aux2);
			aux3<=to_float(0.0,aux3);
			aux4<=to_float(0.0,aux4);
			aux5<=to_float(0.0,aux5);
			aux6<=to_float(0.0,aux6);
			aux7<=to_float(0.0,aux7);
			aux8<=to_float(0.0,aux8);
			aux9<=to_float(0.0,aux9);
			ct1:=0;
			exp_flag<='0';
		else
			
			if data_ready='1' and result=x"FF" and ct=0 and conf_flag='0' then
				ct<=ct+1;
			elsif data_ready='1' and ct=1 then
				cycles(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=2 then
				cycles(7 downto 0)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=3 then
				aux(31 downto 24)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=4 then
				aux(23 downto 16)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=5 then
				aux(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=6 then
				aux(7 downto 0)<=result;
				ct<=ct+1;
			elsif ct=7 then
				time_step<=to_float(aux,time_step);
				ct<=0;
				conf_flag<='1';
			else
				-- nothing happens
			end if;
			
			if data_ready='1' and result=x"EE" and ct=0 then
				rst_flag<='1';
			elsif rst_flag='1' then
				rst_flag<='0';
			else
				-- nothing happens.
			end if;
			
			if ct1>1 and exp_flag='1' then
				ct1:=ct1-1;
			elsif ct1=1 and exp_flag='1' then
				ct1:=ct1-1;
				exp_flag<='0';
			else
				-- nothing happens
			end if;
			
			if conf_flag='1' and timestamp < cycles and count=0 then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux1<=to_float(-3.5,aux1)-Av/to_float(10.0,aux1); --am
				aux2<=to_float(-3.336,aux2)+Av*to_float(-0.0556,aux2); --bm
				aux3<=to_float(-5.0,aux3)-Av/to_float(10.0,aux3); --an
				aux4<=to_float(-0.75,aux4)-Av/to_float(80.0,aux4); --bn
				aux5<=to_float(-0.0008333333333333334,aux5)+Av*to_float(-60.0,aux5); --ah
				aux6<=to_float(-3.0,aux6)+Av*to_float(-0.1,aux6); --bh
				count<=count+1;
				
	
			elsif count=1 then
				exp_data1<=to_slv(aux1);
				exp_data2<=to_slv(aux2);
				exp_data3<=to_slv(aux3);
				exp_data4<=to_slv(aux4);
				exp_data5<=to_slv(aux5);
				exp_data6<=to_slv(aux6);
				--aux1<=aux1;--am
				aux2<=to_float(4.0,aux2); --bm;
				aux3<=aux3/to_float(10.0); --an
				aux4<=to_float(0.125,aux4); --bn;
				aux5<=to_float(0.07,aux5); --ah;
				aux6<=to_float(1.0,aux6); --bh;
				exp_flag<='1';
				ct1:=expDelay;
				count<=count+1;
				
				
			elsif count =2 and exp_flag='0' then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux7<=to_float(1.0,aux7)-to_float(exp_res1,aux7); --am
				aux2<=aux2*to_float(exp_res2,aux2); --bm
				aux8<=to_float(1.0,aux8)-to_float(exp_res3,aux8);-- an
				aux4<=aux4*to_float(exp_res4,aux4); --bn
				aux5<=aux5*to_float(exp_res5,aux5); --ah
				aux9<=to_float(1.0,aux7)+to_float(exp_res6,aux7); --bh
				count<=count+1;
				
			elsif count=3 then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux1<=aux1/aux7; --am
				--aux2<=aux2; -- bm
				aux3<=aux3/aux8; -- an
				--aux4<=aux4; -- bn
				--aux5<=aux5; -- ah
				aux6<=aux6/aux9; --bh
				compute_flag<='1';
				count<=count+1;
				
			elsif count=4 then
				compute_flag<='0';
				count<=count+1;
				
			
			elsif count=5 and rk_flag='1' then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux1<=to_float(-3.5,aux1)-qk/to_float(10.0,aux1); --am
				aux2<=to_float(-3.336,aux2)+qk*to_float(-0.0556,aux2); --bm
				aux3<=to_float(-5.0,aux3)-qk/to_float(10.0,aux3); --an
				aux4<=to_float(-0.75,aux4)-qk/to_float(80.0,aux4); --bn
				aux5<=to_float(-0.0008333333333333334,aux5)+qk*to_float(-60.0,aux5); --ah
				aux6<=to_float(-3.0,aux6)+qk*to_float(-0.1,aux6); --bh
				count<=count+1;
			
			elsif count=6 then
				exp_data1<=to_slv(aux1);
				exp_data2<=to_slv(aux2);
				exp_data3<=to_slv(aux3);
				exp_data4<=to_slv(aux4);
				exp_data5<=to_slv(aux5);
				exp_data6<=to_slv(aux6);
				--aux1<=aux1;--am
				aux2<=to_float(4.0,aux2); --bm;
				aux3<=aux3/to_float(10.0); --an
				aux4<=to_float(0.125,aux4); --bn;
				aux5<=to_float(0.07,aux5); --ah;
				aux6<=to_float(1.0,aux6); --bh;
				exp_flag<='1';
				ct1:=expDelay;
				count<=count+1;
			
			elsif count =7 and exp_flag='0' then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux7<=to_float(1.0,aux7)-to_float(exp_res1,aux7); --am
				aux2<=aux2*to_float(exp_res2,aux2); --bm
				aux8<=to_float(1.0,aux8)-to_float(exp_res3,aux8);-- an
				aux4<=aux4*to_float(exp_res4,aux4); --bn
				aux5<=aux5*to_float(exp_res5,aux5); --ah
				aux9<=to_float(1.0,aux7)+to_float(exp_res6,aux7); --bh
				count<=count+1;
			
			elsif count=8 then
				--am=0.1*(v+35.)/(1-exp(-(v+35)/10.))
				--bm=4.0*exp(-0.0556*(v+60.))
				--an=0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))
				--bn=0.125*exp(-(v + 60.)/80.)
				--ah=0.07*exp(-0.05*(v + 60.))
				--bh=1./(1+exp(-(0.1)*(v + 30.)))
				aux1<=aux1/aux7; --am
				--aux2<=aux2; -- bm
				aux3<=aux3/aux8; -- an
				--aux4<=aux4; -- bn
				--aux5<=aux5; -- ah
				aux6<=aux6/aux9; --bh
				compute_flag<='1';
				count<=count+1;
				
			elsif count=9 then
				compute_flag<='0';
				count<=count+1;
			
			elsif count=10 and rk_flag='1' then
					we<='1';
					queue<=qAux+1;
					waddr<=qAux;
					qAux<=qAux+1;
					data(55 downto 40)<=std_logic_vector(to_unsigned(timestamp,16));
					data(39 downto 8)<=to_slv(aV);
					data(7 downto 1)<=(others =>'0');
					data(0)<=spike;
					count<=count+1;
				
			elsif count=11 then
					we<='0';
					count<=0;
					timestamp<=timestamp+1;
					debug<=std_logic_vector(to_unsigned(timestamp,8));
			else
			-- nothing happens
			end if;
			rst<=rst_flag;
		end if;	
		else
			-- nothing happens
		end if;
	end process;
	
	process(clk, reset, timestamp, aux1, aux2, aux3, aux4, aux5, aux6, compute_flag)
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			Vm<=to_float(-60.0,Vm);
			Cm<=to_float(0.01,Cm);
			dt<=to_float(0.05,dt);
			Av<=to_float(0.0,Av);
			Av_1<=to_float(0.0,Av_1);
			Av_2<=to_float(0.0,Av_2);
			spike<='0';
			h<=to_float(0.0,h);
			m<=to_float(0.0,m);
			n<=to_float(0.0,n);
			k1<=to_float(0.0,k1);
			m1<=to_float(0.0,m1);
			n1<=to_float(0.0,n1);
			h1<=to_float(0.0,h1);
			qk<=to_float(0.0,qk);
			qm<=to_float(0.0,qm);
			qn<=to_float(0.0,qn);
			qh<=to_float(0.0,qh);
			k2<=to_float(0.0,k2);
			m2<=to_float(0.0,m2);
			n2<=to_float(0.0,n2);
			h2<=to_float(0.0,h2);
			IK<=to_float(0.0,IK);
			INa<=to_float(0.0,INa);
			Il<=to_float(0.0,Il);
			I<=to_float(0.1,I);
			countRK<=0;
			rk_flag<='0';
			ENa<=to_float(55.17,ENa);
			EK<=to_float(-72.14,EK);
			El<=to_float(-49.42,El);
			gbarNa<=to_float(1.2,gbarNa);
			gbarK<=to_float(0.36,gbarK); 
			gbarl<=to_float(0.003,gbarl);
			gNa<=to_float(0.0,gNa);
			gK<=to_float(0.0,gK); 
			gl<=to_float(0.0,gl);
			aux10<=to_float(0.0,aux10);
			aux11<=to_float(0.0,aux11);
			aux12<=to_float(0.0,aux12);
		else
			if countRK=0 and compute_flag='1' then
--				v = y[0]
--				n = y[1]
--				m = y[2]
--				h = y[3]
				Av_2<=Av_1;
				Av_1<=Av;
				if timestamp = 0 then
					Av<=Vm;
					m<=to_float(0.052932485257249577,m);
					n<=to_float(0.31767691406069742,n);
					h<=to_float(0.59612075350846028,h);
				else
					-- nothing happens
				end if;
				countRK<=countRK+1;
			
			elsif countRK=1 then
--				gNa=gbarNa*(m**3)*h
--				gK=gbarK*(n**4)
--				gl=gbarl
				aux10<=m*m*m;
				aux11<=n*n*n;
				gNa<=gbarNa*h;
				gl<=gbarl;
				gK<=gbarK*n;
				countRK<=countRK+1;
			
			elsif countRK=2 then
--				INa=gNa*(v-ENa)
--				IK=gK*(v-EK)
--				Il=gl*(v-El)
				gNa<=gNa*aux10;
				gK<=gK*aux11;
				INa<=aV-ENa;
				IK<=aV-EK;
				Il<=aV-El;
				countRK<=countRK+1;
			
			elsif countRK=3 then
--				INa=gNa*(v-ENa)
--				IK=gK*(v-EK)
--				Il=gl*(v-El)
				INa<=INa*gNa;
				IK<=IK*gK;
				Il<=Il*gl;
--				k1 = ((1/Cm)*(I(i)-(INa+IK+Il)))
--				n1 = an(v)*(1-n)-bn(v)*n
--				m1 = am(v)*(1-m)-bm(v)*m
--				h1 = ah(v)*(1-h)-bh(v)*h
				k1<=I/Cm;
				m1<=aux1*to_float(1.0,m1)-aux1*m;
				aux10<=aux2*m;
				n1<=aux3*to_float(1.0,n1)-aux3*n;
				aux11<=aux4*n;
				h1<=aux5*to_float(1.0,h1)-aux5*h;
				aux12<=aux6*h;
				countRK<=countRK+1;
			
			elsif countRK=4 then
--				k1 = ((1/Cm)*(I(i)-(INa+IK+Il)))
--				n1 = an(v)*(1-n)-bn(v)*n
--				m1 = am(v)*(1-m)-bm(v)*m
--				h1 = ah(v)*(1-h)-bh(v)*h
				k1<=k1-INa-IK-Il;
				m1<=m1-aux10;
				n1<=n1-aux11;
				h1<=h1-aux12;
--				qk1 = V[i] + dt*(0.5*k1)
--				qn1 = n[i] + dt*(0.5*n1)
--				qm1 = m[i] + dt*(0.5*m1)
--				qh1 = h[i] + dt*(0.5*h1)
				qk<=dt*to_float(0.5,qk);
				qm<=dt*to_float(0.5,qm);
				qn<=dt*to_float(0.5,qn);
				qh<=dt*to_float(0.5,qh);
				countRK<=countRK+1;
				
			elsif countRK=5 then
--				qk1 = V[i] + dt*(0.5*k1)
--				qn1 = n[i] + dt*(0.5*n1)
--				qm1 = m[i] + dt*(0.5*m1)
--				qh1 = h[i] + dt*(0.5*h1)
				qk<=aV+qk*k1;
				qm<=m+qm*m1;
				qn<=n+qn*n1;
				qh<=h+qh*h1;
--				INa=gNa*(v-ENa)
--				IK=gK*(v-EK)
--				Il=gl*(v-El)
				INa<=qk-ENa;
				IK<=qk-EK;
				Il<=qk-El;
				rk_flag<='1';
				countRK<=countRK+1;
				
			elsif countRK=6 then
--				k2 = ((1/Cm)*(I(i)-(INa+IK+Il)))
--				n2 = an(qk)*(1-n)-bn(qk)*n
--				m2 = am(qk)*(1-m)-bm(qk)*m
--				h2 = ah(qk)*(1-h)-bh(qk)*h
				k2<=I/Cm;
				rk_flag<='0';
				countRK<=countRK+1;
			
			elsif countRK=7 and compute_flag='1' then
--				k2 = ((1/Cm)*(I(i)-(INa+IK+Il)))
--				n2 = an(qk)*(1-n)-bn(qk)*n
--				m2 = am(qk)*(1-m)-bm(qk)*m
--				h2 = ah(qk)*(1-h)-bh(qk)*h
				k2<=k2-INa-IK-Il;
				m2<=aux1*to_float(1.0,m2)-aux1*m;
				aux10<=aux2*m;
				n2<=aux3*to_float(1.0,n2)-aux3*n;
				aux11<=aux4*n;
				h2<=aux5*to_float(1.0,h2)-aux5*h;
				aux12<=aux6*h;
				countRK<=countRK+1;
				
			elsif countRK=8 then
--				k2 = ((1/Cm)*(I(i)-(INa+IK+Il)))
--				n2 = an(qk)*(1-n)-bn(qk)*n
--				m2 = am(qk)*(1-m)-bm(qk)*m
--				h2 = ah(qk)*(1-h)-bh(qk)*h
				--k2<=k2;
				m2<=m2-aux10;
				n2<=n2-aux11;
				h2<=h2-aux12;	
				countRK<=countRK+1;
				
			elsif countRK=9 then
--				V[i+1] = V[i] + dt*k2
--				n[i+1] = n[i] + dt*n2
--				m[i+1] = m[i] + dt*m2 
--				h[i+1] = h[i] + dt*h2
				Av<=Av+dt*k2;
				m<=m+dt*m2;
				n<=n+dt*n2;
				h<=h+dt*h2;
				countRK<=countRK+1;
				if Av<Av_1 and Av_1>Av_2 then
					spike<='1';
				else
					spike<='0';
				end if;
				rk_flag<='1';
				
			elsif countRK=10 then
				countRK<=0;
				rk_flag<='0';
			else
				--nothing happens
			end if;
		end if;
	else
		-- nothing happens
	end if;
	end process;
	
	
end HH_arch;