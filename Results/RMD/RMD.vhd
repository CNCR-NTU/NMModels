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

entity RMD is

generic 
	(
		DATA_WIDTH : natural := 56;
		ADDR_WIDTH : natural := 32;
		SPIKE:		 natural := 304
	);

port (clk		: IN std_logic;
		reset		: IN std_logic;
		data_ready: IN std_logic;
		result	: IN	STD_LOGIC_VECTOR (7 downto 0);
		exp_res1	: IN	STD_LOGIC_VECTOR (31 downto 0);
		exp_res2	: IN	STD_LOGIC_VECTOR (31 downto 0);
		abs_res 	: IN	STD_LOGIC_VECTOR (31 downto 0);
		waddr		: OUT std_logic_vector((ADDR_WIDTH-1) downto 0);
		data		: OUT std_logic_vector((DATA_WIDTH-1) downto 0);
		we			: OUT std_logic;
		queue		: out std_logic_vector((ADDR_WIDTH-1) downto 0);
		rst		: OUT std_logic;
		exp_data1	: out	STD_LOGIC_VECTOR (31 downto 0);
		exp_data2	: out	STD_LOGIC_VECTOR (31 downto 0);
		abs_data	:  out		STD_LOGIC_VECTOR (31 downto 0);
		debug		: OUT std_logic_vector (7 downto 0)
		);
end RMD;

-- architecture body --
architecture RMD_arch of RMD is

constant	expDelay:		natural									:=17;
signal 	A:					float32;
signal 	B:					float32;
signal 	C:					float32;
signal 	D:					float32;
signal 	m:					float32;
signal 	dt:				float32;
signal 	stim:				float32;
signal 	v1:				float32;
signal	Vm:				float32;
signal	Vm2:				float32;
signal	Vm1:				float32;
signal	Ap:				float32;
signal	Ap_last:				float32;
signal 	stim_last:		float32;
signal	step:				float32;
signal	x:					float32;
signal	x1:				float32;
signal	x2:				float32;
signal	aux1:				float32;
signal	aux2:				float32;
signal	aux3:				float32;
signal	iflag:			std_logic 								:='0';
signal	exp_flag:		std_logic 								:='0';
signal	aux4:				float32;
signal	aux5:				float32;
signal	aux6:				float32;
signal	exp_data1_aux:	float32;
signal	exp_data2_aux:	float32;
signal	s:					std_logic_vector(31 downto 0):=(others =>'0');
signal 	qAux:				std_logic_vector((ADDR_WIDTH-1) downto 0):=(others =>'0');
signal 	ct:				natural									:=0;
signal 	count:			natural									:=0;
signal	rst_flag: 		std_logic								:='0';
signal	conf_flag:		std_logic 								:='0';
signal	compute_flag:	std_logic 								:='0';
signal 	cycles:			std_logic_vector (15 downto 0)   :=(others=>'0');
signal 	timestamp:		natural									:=0;
signal	K1:				float32;
signal 	q:				float32;
signal	K2:				float32;
signal 	countRK:			natural									:=0;
signal	rk_flag:			std_logic 								:='0';

		--- process ---
BEGIN
	process(clk, reset, Ap, rk_flag)
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			conf_flag<='0';
			ct<=0;
			count<=0;
			rst_flag<='0';
			cycles<=(others =>'0');
			timestamp<=0;
			compute_flag<='0';
			we<='0';
			data<=(others => '0');
			waddr<=(others => '0');
			queue<=(others =>'0');
			qAux<=(others =>'0');
		else
			
			if data_ready='1' and result=x"FF" and ct=0 and conf_flag='0' then
				ct<=ct+1;
			elsif data_ready='1' and ct=1 then
				cycles(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=2 then
				cycles(7 downto 0)<=result;
				ct<=ct+1;
			elsif ct=3 then
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
			
			if conf_flag='1' and timestamp < cycles and count=0 then
				compute_flag<='1';
				count<=count+1;
				
			elsif count=1 then
				compute_flag<='0';	
				count<=count+1;

			elsif count=2 and rk_flag='1' then
				we<='1';
				queue<=qAux+1;
				waddr<=qAux;
				qAux<=qAux+1;
				data(55 downto 40)<=std_logic_vector(to_unsigned(timestamp,16));
				data(39 downto 8)<=to_slv(Ap);
				data(7 downto 0)<=(others =>'0');
				count<=count+1;
				
			elsif count=3 then
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
	
	process(clk, reset, compute_flag)
	variable ct1: natural :=0;
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			dt<=to_float(0.025,dt);
			v1<=to_float(0.0,v1);
			countRK<=0;
			rk_flag<='0';
			K1<=to_float(0.0,K1);
			K2<=to_float(0.0,K2);
			q<=to_float(0.0,q);
			aux2<=to_float(0.00,aux2);
			aux3<=to_float(0.00,aux3);
			ct1:=0;
			exp_flag<='0';
			abs_data<=(others =>'0');
			stim_last<=to_float(0.0,stim_last);
			stim<=to_float(0.0,stim);
			step<=to_float(0.05,step);
			x<=to_float(0.0,x);
			x1<=to_float(0.0,x1);
			x2<=to_float(0.0,x2);
			s<=(others =>'0');
			aux1<=to_float(0.0,aux1);
			aux5<=to_float(0.0,aux5);
			aux4<=to_float(0.0,aux4);
			aux6<=to_float(0.0,aux6);
			exp_data1_aux<=to_float(0.0,exp_data1_aux);
			exp_data2_aux<=to_float(0.0,exp_data2_aux);
			exp_data1<=(others=>'0');
			exp_data2<=(others=>'0');
			iflag<='0';
			A<=to_float(0.0,A);
			B<=to_float(0.0,B);
			C<=to_float(126.66,C);
			D<=to_float(0.0,D);
			m<=to_float(0.0,m);
			Vm1<=to_float(-70.0,Vm1);
			Vm2<=to_float(-35.0,Vm2);
			Vm<=to_float(0.0,Vm);
			Ap<=to_float(0.0,Ap);
			Ap_last<=to_float(0.0,Ap_last);
		else
			
			if ct1>1 and exp_flag='1' then
				ct1:=ct1-1;
			elsif ct1=1 and exp_flag='1' then
				ct1:=ct1-1;
				exp_flag<='0';
			else
				-- nothing happens
			end if;
			
			if countRK=0 and compute_flag='1' then
				stim_last<=stim;
				if (timestamp>=100 and timestamp<=500) then
					stim<=to_float(10.0,stim);
				elsif (timestamp>=800 and timestamp<=1000) then
					stim<=to_float(-10.0,stim);
				else
					stim<=to_float(0.0,stim);
				end if;
				
				if timestamp=0 then
					Ap<=Vm1;
					Vm<=Vm2;
					s<=(others =>'0');
					x<=to_float(0.0,x);
					stim_last<=to_float(0.0,stim_last);
				else
					Ap_last<=Ap;
					Ap<=to_float(0.0,Ap);
				end if;
				-- f(s)=1/(1+exp(-0.001*t))
				aux1<=to_float(-0.7376,aux1); -- A
				aux4<=to_float(-0.001,aux4);  -- f
				aux5<=to_float(-2.258,aux5);  -- D
				countRK<=countRK+1;	
			
			elsif countRK=1 then
				--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
				--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				--C=126.66
				--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x1-Vm*x2-0.1244
				if stim<to_float(0.0,stim) or stim>to_float(0.0,stim) then
					iflag<='0';
					A<=to_float(-0.3341,A);
					B<=to_float(-15.28,B)*stim_last+to_float(79.42,B);
					aux1<=stim_last*stim_last; -- B
					aux2<=to_float(2.0,aux2)*stim_last; -- x1 and x2
					aux4<=to_float(0.04412,aux4); --B
					aux5<=to_float(-0.18072,aux5)*stim_last; --B
					aux6<=to_float(0.5936,aux6); -- B
					C<=to_float(126.66,C);
					D<=to_float(-0.1244,D);
					exp_data1_aux<=aux1*stim_last;
					exp_data2_aux<=aux5*stim;
					abs_data<=to_slv(stim_last);
				else
--					-- f(s)=1/(1+exp(-0.001*s))
--					iflag<='1';
--					x<=to_float(0.0,x); 
--					if stim<stim_last or stim>stim_last then
--						s<=(others =>'0');
--						exp_data1_aux<=to_float(0.0,exp_data1_aux);
--					else
--						exp_data1_aux<=to_float(s,exp_data1_aux)*aux4;
--						--nothing happens
--					end if;
--					if Ap_last>=Vm2 then
--						-- V[t+1]=0.1*(Vm2-V[t])*f(s)+V[t]
--						aux1<=Vm2-Ap_last; -- Vm2 - V[t]
--						s<=s+1;
--					elsif Ap_last<Vm2 then
--						-- V[t+1]=0.1*(Vm1-V[t])*f(s)+V[t]
--						aux1<=Vm1-Ap_last; -- Vm1 - V[t]
--						s<=s+1;
--					end if;
				end if;
				countRK<=countRK+1;
				
			elsif countRK=2 then
				if iflag='0' then
					--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
					--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
					--C=126.66
					--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x1-Vm*x2-0.1244
					x2<=to_float(abs_res,x2)/aux2-stim_last/aux2; -- abs(I(t))-I(t))/(2*I(t))
					x1<=to_float(abs_res,x1)/aux2+stim_last/aux2; -- abs(I(t))+I(t))/(2*I(t))
					B<=aux1+B; --I(t)**2-15.28*I(t)+79.42
					aux4<=aux4*aux1; --0.04412*I(t)**2
					aux5<=aux5+aux6; -- -0.18072*I(t)+0.5936
					if Vm=Vm2 then
						m<=to_float(0.93,m);
					else
						m<=to_float(0.4,m);
					end if;
					exp_data1<=to_slv(exp_data1_aux);
					exp_data2<=to_slv(exp_data2_aux);
					countRK<=countRK+1;
				else
--					-- f(s)=1/(1+exp(-0.001*s))
--					-- V[t+1]=0.1*(Vm_1or2-V[t])*f(s)+V[t]
--					exp_data1<=to_slv(exp_data1_aux);
--					aux1<=aux1*to_float(0.1,aux1); --0.1*(Vm_1or2-V[t])
--					aux4<=to_float(1.0,aux4);
--					countRK<=6; -- jump to 6
				end if;
				exp_flag<='1';
				ct1:=expDelay;
				
			elsif countRK=3 then
				--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
				--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				--C=126.66
				--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x-Vm*x-0.1244
				aux4<=aux4+aux5; -- 0.04412*I(t)**2-0.18072*I(t)+0.5936
				aux5<=to_float(0.0179, aux5); --A
				aux6<=to_float(1.711e-6, aux6); -- D
				D<=to_float(-70.0,D)*x1+D; -- -70*x1-0.1244
				A<=m*x2+A; --m*x2-0.3341
				countRK<=countRK+1;
				
			elsif countRK=4 then	
				--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
				--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				--C=126.66
				--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x-Vm*x-0.1244
				B<=aux4*x1/B; -- ((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1
				aux4<=to_float(-0.04,aux4)*x2; -- -0.04*x2
				D<=-Vm*x2+D; -- -70*x1-Vm*x2-0.1244
				countRK<=countRK+1;
				
				
			elsif countRK=5 then		
				--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
				--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				--C=126.66
				--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x-Vm*x-0.1244
				B<=B+aux4; --B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				countRK<=countRK+1;
				
			elsif countRK=6 and exp_flag='0' then
				if iflag='0' then
					aux1<=to_float(-0.04166,aux1)*x1; -- -0.04166*x1
					aux5<=aux5+to_float(exp_res1,aux5); -- 0.0179+exp(-0.7376*I(t)
					aux6<=aux6+to_float(exp_res2,aux6); -- 1.711e-6+exp(-2.258*I(t))
					exp_data1_aux<=to_float(-0.7376,aux1);
					exp_flag<='1';
					ct1:=expDelay;
				else
--					-- f(s)=1/(1+exp(-0.001*s))
--					-- V[t+1]=0.1*(Vm_1or2-V[t])*f(s)+V[t]
--					aux4<=aux4+to_float(exp_res1,aux4);
				end if;
				countRK<=countRK+1;
				
				
			elsif countRK=7 then	
				if iflag='0' then
					--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
					--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
					--C=126.66
					--D = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))-70*x-Vm*x-0.1244
					A<=aux1/aux5+A;
					aux2<=to_float(2.0,aux2)*stim_last; -- x1 and x2
					D<=to_float(7.851e-5,D)/aux6+D;
					abs_data<=to_slv(stim);
				else
					-- f(s)=1/(1+exp(-0.001*s))
					-- V[t+1]=0.1*(Vm_1or2-V[t])*f(s)+V[t]
					aux4<=to_float(1.0,aux4)/aux4; -- f(s)
				end if;
				countRK<=countRK+1;
				
			elsif countRK=8 then		
				if iflag='0' then
					K1<=A*x+B*stim_last;
					--A = -0.04166/(0.0179+exp(-0.7376*I(t)))*x1+m*x2-0.3341
					--B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
					x2<=to_float(abs_res,x2)/aux2-stim/aux2; -- abs(I(t))-I(t))/(2*I(t))
					x1<=to_float(abs_res,x1)/aux2+stim/aux2; -- abs(I(t))+I(t))/(2*I(t))
					A<=to_float(-0.3341,A);
					B<=to_float(-15.28,B)*stim_last+to_float(79.42,B);
					aux1<=stim_last*stim_last; -- B
					aux4<=to_float(0.04412,aux4); --B
					aux5<=to_float(-0.18072,aux5)*stim_last; --B
					aux6<=to_float(0.5936,aux6); -- B
					countRK<=countRK+1;
				else
--					-- f(s)=1/(1+exp(-0.001*s))
--					-- V[t+1]=0.1*(Vm_1or2-V[t])*f(s)+V[t]
--					Ap<=aux1*aux4+Ap_last; -- V[t+1]=0.1*(Vm_1or2-V[t])*f(s)+V[t]
--					rk_flag<='1';
--					countRK<=18; -- jump to set rk_flag<='0'   <################################
				end if;
				
			elsif countRK=9 then			
				q<=x+k1*dt;
				B<=aux1+B; --I(t)**2-15.28*I(t)+79.42
				aux4<=aux4*aux1; --0.04412*I(t)**2
				aux5<=aux5+aux6; -- -0.18072*I(t)+0.5936
				countRK<=countRK+1;
			
			elsif countRK=10 then		
				aux4<=aux4+aux5; -- 0.04412*I(t)**2-0.18072*I(t)+0.5936
				aux5<=to_float(0.0179, aux5); --A
				A<=m*x2+A; --m*x2-0.3341
				countRK<=countRK+1;
			
			elsif countRK=11 then	
				B<=aux4*x1/B; -- ((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1
				aux4<=to_float(-0.04,aux4)*x2; -- -0.04*x2
				countRK<=countRK+1;
				
			elsif countRK=12 then		
				B<=B+aux4; --B=((0.04412*I(t)**2-0.18072*I(t)+0.5936)/(I(t)**2-15.28*I(t)+79.42))*x1-0.04*x2
				countRK<=countRK+1;
				
			elsif countRK=13 and exp_flag='0' then
				aux1<=to_float(-0.04166,aux1)*x1; -- -0.04166*x1
				aux5<=aux5+to_float(exp_res1,aux5); -- 0.0179+exp(-0.7376*I(t)
				countRK<=countRK+1;
			
			elsif countRK=14 then
				A<=aux1/aux5+A;
				countRK<=countRK+1;
			
			elsif countRK=15 then	
				K2<=A*q+B*stim;
				countRK<=countRK+1;
				
			elsif countRK=16 then
				x<=x+K2*to_float(0.05,x);
				countRK<=countRK+1;
				
				
			elsif countRK=17 then
				Ap<=C*x+D;
				countRK<=countRK+1;
				rk_flag<='1';
				
			elsif countRK=18 then
				rk_flag<='0';
				countRK<=0;
				--V[t+1] = C(t)*x + D(t)
			else
				--nothing happens
			end if;
		end if;
	else
		-- nothing happens
	end if;
	end process;
end RMD_arch;
