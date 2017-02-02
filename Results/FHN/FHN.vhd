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

entity FHN is

generic 
	(
		DATA_WIDTH : natural := 56;
		ADDR_WIDTH : natural := 32
	);

port (clk		: IN std_logic;
		reset		: IN std_logic;
		data_ready: IN std_logic;
		result	: IN	STD_LOGIC_VECTOR (7 downto 0);
		waddr		: OUT std_logic_vector((ADDR_WIDTH-1) downto 0);
		data		: OUT std_logic_vector((DATA_WIDTH-1) downto 0);
		we			: OUT std_logic;
		queue		: out std_logic_vector((ADDR_WIDTH-1) downto 0);
		rst		: OUT std_logic;
		debug		: OUT std_logic_vector (7 downto 0)
		);
end FHN;

-- architecture body --
architecture FHN_arch of FHN is
signal 	A:					float32;
signal	B:					float32;
signal	tau:				float32;
signal	w: 				float32;
signal	v: 				float32;
signal 	dt:				float32;
signal	Vm:				float32;
signal	Ap:				float32;
signal	Ap_1:				float32;
signal	Ap_2:				float32;
signal	stim:				float32;
signal	stim_last:		float32;
signal 	qAux:				std_logic_vector((ADDR_WIDTH-1) downto 0):=(others =>'0');
signal 	ct:				natural									:=0;
signal 	count:			natural									:=0;
signal	rst_flag: 		std_logic								:='0';
signal	conf_flag:		std_logic 								:='0';
signal	compute_flag:	std_logic 								:='0';
signal 	cycles:			std_logic_vector (15 downto 0)   :=(others=>'0');
signal 	timestamp:		natural									:=0;
signal	K1:				float32;
signal 	q:					float32;
signal	K2:				float32;
signal 	countRK:			natural									:=0;
signal	rk_flag:			std_logic 								:='0';
signal	aux:				std_logic_vector (31 downto 0)   :=(others=>'0');
signal	spike:			std_logic 								:='0';


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
			stim<=to_float(0.0,stim);
			v<=to_float(0.0,v);
			aux<=(others=>'0');
			stim<=to_float(0.0,stim);
			stim_last<=to_float(0.0,stim_last);
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
			elsif data_ready='1' and ct=7 then
				a<=to_float(aux,a);
				aux(31 downto 24)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=8 then
				aux(23 downto 16)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=9 then
				aux(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=10 then
				aux(7 downto 0)<=result;
				ct<=ct+1;	
			elsif ct=11 then
				b<=to_float(aux,b);
				aux(31 downto 24)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=8 then
				aux(23 downto 16)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=9 then
				aux(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=10 then
				aux(7 downto 0)<=result;
				ct<=ct+1;	
			elsif ct=11 then
				tau<=to_float(aux,tau);
				ct<=0;
				conf_flag<='1';
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
				stim_last<=stim;
				if (timestamp>=0 and timestamp<=4000) then
					stim<=to_float(0.6,stim);
				else
					stim<=to_float(0.0,stim);
				end if;
				
				count<=count+1;
				
			elsif count=1 then
				compute_flag<='1';
				count<=count+1;
				
			elsif count=3 then
				compute_flag<='0';
				count<=count+1;
			
			elsif count=4 and rk_flag='1' then
				v<=to_float(45.0,v);
				count<=count+1;
			
			elsif count=5 then
				we<='1';
				queue<=qAux+1;
				waddr<=qAux;
				qAux<=qAux+1;
				data(55 downto 40)<=std_logic_vector(to_unsigned(timestamp,16));
				data(39 downto 8)<=to_slv(v);
				data(7 downto 1)<=(others =>'0');
				data(0)<=spike;
				count<=count+1;
				
			elsif count=6 then
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
	
	process(clk, reset, compute_flag, stim, stim_last)
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			countRK<=0;
			w<=to_float(0.0,w);
			rk_flag<='0';
			K1<=to_float(0.0,K1);
			K2<=to_float(0.0,K2);
			q<=to_float(0.0,q);
			Ap<=to_float(0.0,Ap);
			Ap_1<=to_float(0.0,Ap_1);
			Ap_2<=to_float(0.0,Ap_2);
			dt<=to_float(0.025,dt);
		else
			if countRK=0 and compute_flag='1' then
				--v=v - v**3 - w + I(t)
				--w=(v + a - b*w)/tau
				K1<=Ap-Ap*Ap*Ap-w+stim_last;
				Ap_2<=Ap_1;
				Ap_1<=Ap;
				countRK<=countRK+1;
				
			elsif countRK=1 then
				q<=Ap+K1*dt;
				countRK<=countRK+1;
			
			elsif countRK=2 then
				K2<=q-q*q*q-w+stim;
				K1<=Ap+a-b*w;
				countRK<=countRK+1;
				
			elsif countRK=3 then
				Ap<=Ap+to_float(0.05,Ap)*K2;
				K1<=K1/tau;
				countRK<=countRK+1;
				
			elsif countRK=4 then
				q<=w+K1*dt;
				K2<=Ap+a-b*w;
				countRK<=countRK+1;
				
			elsif countRK=5 then
				K2<=K2/tau;
				countRK<=countRK+1;
			
			elsif countRK=6 then
				w<=w+K2*to_float(0.05,w);
				countRK<=countRK+1;
				if Ap<Ap_1 and Ap_1>Ap_2 then
					spike<='1';
				else
					spike<='0';
				end if;
				rk_flag<='1';
				
			elsif countRK=7 then
				rk_flag<='0';
				countRK<=0;
			else
				--nothing happens
			end if;
		end if;
	else
		-- nothing happens
	end if;
	end process;
end FHN_arch;