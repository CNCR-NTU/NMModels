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

entity WMM is

generic 
	(
		DATA_WIDTH : natural := 56;
		ADDR_WIDTH : natural := 16;
		SPIKE:		 natural := 304
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
end WMM;

-- architecture body --
architecture WMM_arch of WMM is

signal 	k:					float32;
signal 	A:					float32;
signal 	B:					float32;
signal 	C:					float32;
signal 	D:					float32;
signal 	dt:				float32;
signal 	stim:				float32;
signal 	v1:				float32;
signal 	v2:				float32;
signal	forces:			float32;
signal	forces_aux:		float32;
signal	spikeTrain:		std_logic_vector (SPIKE-1 downto 0)	:=(others=>'0');
signal 	qAux:				std_logic_vector((ADDR_WIDTH-1) downto 0):=(others =>'0');
signal 	ct:				natural									:=0;
signal 	count:			natural									:=0;
signal	rst_flag: 		std_logic								:='0';
signal	conf_flag:		std_logic 								:='0';
signal	compute_flag:	std_logic 								:='0';
signal 	cycles:			std_logic_vector (15 downto 0)   :=(others=>'0');
signal 	timestamp:		natural									:=0;
signal	M1A:				float32;
signal 	M1B:				float32;
signal	M1C:				float32;
signal 	M1D:				float32;
signal	M2A:				float32;
signal 	M2B:				float32;
signal	K1A:				float32;
signal 	K1B:				float32;
signal	q1A:				float32;
signal	q1B:				float32;
signal	K2A:				float32;
signal	K2B:				float32;
signal	q2A:				float32;
signal	q2B:				float32;
signal	K3A:				float32;
signal	K3B:				float32;
signal	q3A:				float32;
signal	q3B:				float32;
signal	K4A:				float32;
signal	K4B:				float32;
signal	rkAux0:			float32;
signal	rxAux1:			float32;
signal	rkAux2:			float32;
signal	rxAux3:			float32;
signal 	countRK:			natural									:=0;
signal	rk_flag:			std_logic 								:='0';


function train2spk(spikeTrain: std_logic_vector (SPIKE-1 downto 0)) return std_logic_vector is
	variable spikes: std_logic_VECTOR(15 downto 0) := (others =>'0');
	begin
		for I in 0 to SPIKE-1 loop
			if spikeTrain(i)='1' then
				spikes:=x"0001";
			else
				-- do nothing
			end if;
		end loop;
		return spikes;
	end train2spk;

		--- process ---
BEGIN
	process(clk, reset, v1, v2, stim, rk_flag)
	variable aux     : float32;
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			forces<=to_float(0.0,forces);
			forces_aux<=to_float(0.0,forces_aux);
			conf_flag<='0';
			ct<=0;
			count<=0;
			rst_flag<='0';
			cycles<=(others =>'0');
			timestamp<=0;
			spikeTrain<=(others =>'0');
			compute_flag<='0';
			we<='0';
			data<=(others => '0');
			waddr<=(others => '0');
			queue<=(others => '0');
			qAux<=(others =>'0');
			aux:=to_float(0.0,aux);
			k<=to_float(0.53,k);
		else
			
			if data_ready='1' and result=x"FF" and ct=0 and conf_flag='0' then
				ct<=ct+1;
			elsif data_ready='1' and ct=1 then
				cycles(15 downto 8)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct=2 then
				cycles(7 downto 0)<=result;
				ct<=ct+1;
			elsif data_ready='1' and ct>2 and ct<41 then
				spikeTrain((SPIKE-1-(ct-3)*8) downto (SPIKE-8-(ct-3)*8))<=result;
				ct<=ct+1;
			elsif ct=41 then
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
				forces<=v1*v1*v1;
				count<=count+1;

			elsif count=3 then
				forces<=forces*v1*v1;
				count<=count+1;
			
			elsif count=4 then
				forces<=forces+to_float(0.04181954930000001,forces);
				aux:=forces;
				count<=count+1;

			elsif count=5 then
				forces<=to_float(100.0,forces)*aux/forces;
				count<=count+1;
			

			elsif count=6 then
				we<='1';
				queue<=qAux+1;
				waddr<=qAux;
				qAux<=qAux+1;
				data(55 downto 40)<=std_logic_vector(to_unsigned(timestamp,16));
				data(39 downto 8)<=to_slv(forces);
				data(7 downto 0)<=(others =>'0');
				count<=count+1;
			
			elsif count=7 then
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
	
	process(clk, reset, compute_flag, timestamp)
	begin
	if clk'event and clk='1' then 
		if reset='1' then
			A<=to_float(1.0,A);
			B<=to_float(25.0,B);
			C<=to_float(-0.015,C);
			D<=to_float(14.0,D);
			dt<=to_float(0.05,dt);
			stim<=to_float(1.0,stim);
			v1<=to_float(0.0,v1);
			v2<=to_float(0.0,v2);
			countRK<=0;
			rk_flag<='0';
			K1A<=to_float(0.0,K1A);
			K1B<=to_float(0.0,K1B);
			K2A<=to_float(0.0,K2A);
			K2B<=to_float(0.0,K2B);
			K3A<=to_float(0.0,K3A);
			K3B<=to_float(0.0,K3B);
			K4A<=to_float(0.0,K4A);
			K4B<=to_float(0.0,K4B);
			q1A<=to_float(0.0,q1A);
			q1B<=to_float(0.0,q1B);
			q2A<=to_float(0.0,q2A);
			q2B<=to_float(0.0,q2B);
			q3A<=to_float(0.0,q3A);
			q3B<=to_float(0.0,q3B);
			M1A<=to_float(0.0,M1A);
			M1B<=to_float(0.0,M1B);
			M1C<=to_float(0.0,M1C);
			M1D<=to_float(0.0,M1D);
			M2A<=to_float(0.0,M2A);
			M2B<=to_float(0.0,M2B);
			rkAux0<=to_float(0.0,rkAux0);
			rxAux1<=to_float(0.0,rxAux1);
			rkAux2<=to_float(0.0,rkAux2);
			rxAux3<=to_float(0.0,rxAux3);
		else
			if countRK=0 and compute_flag='1' then
				if timestamp>=100 and timestamp<=600 then
					stim<=to_float(unsigned(train2spk(spikeTrain)),stim);
				else
					stim<=(others =>'0');
				end if;
				M1A<= to_float(0.0,M1A);
				M1B<= -C;
				M1C<= -B;
				M1D<= -A;
				M2A<= to_float(0.0,M2A);
				M2B<= D;
				countRK<=countRK+1;
			
			elsif countRK=1 then
				K1A<=M1B*v2+M2A*stim;
				K1B<=M1D*v2+M2B*stim;
				countRK<=countRK+1;
			
			elsif countRK=2 then
				K1A<=M1A*v1 + K1A;
				K1B<=M1C*v1 + K1B;
				q1A<=dt*to_float(0.5,q1A);
				q1B<=dt*to_float(0.5,q1B);
				countRK<=countRK+1;
			
			elsif countRK=3 then
				q1A<=v1+K1A*q1A;
				q1B<=v2+K1B*q1B;
				K2A<=M2A*stim;
				K2B<=M2B*stim;
				countRK<=countRK+1;
				
			elsif countRK=4 then
				K2A<=M1B*q1B+K2A;
				K2B<=M1D*q1B+K2B;
				countRK<=countRK+1;
			
			elsif countRK=5 then
				K2A<=M1A*q1A+K2A;
				K2B<=M1C*q1A+K2B;
				q2A<=dt*to_float(0.5,q2A);
				q2B<=dt*to_float(0.5,q2B);
				countRK<=countRK+1;
				
			elsif countRK=6 then
				q2A<=v1+K2A*q2A;
				q2B<=v2+K2B*q2B;
				K3A<=M2A*stim;
				K3B<=M2B*stim;
				countRK<=countRK+1;
				
			elsif countRK=7 then
				K3A<=M1B*q2B+K3A;
				K3B<=M1D*q2B+K3B;
				countRK<=countRK+1;
				
			elsif countRK=8 then
				K3A<=M1A*q2A + K3A;
				K3B<=M1C*q2A + K3B;
				q3A<=dt*to_float(0.5,q2A);
				q3B<=dt*to_float(0.5,q2B);
				countRK<=countRK+1;
				
			elsif countRK=9 then
				q3A<=v1+K3A*q3A;
				q3B<=v2+K3B*q3B;
				K4A<=M2A*stim;
				K4B<=M2B*stim;
				countRK<=countRK+1;
				
			elsif countRK=10 then
				K4A<=M1B*q3B+K4A;
				K4B<=M1D*q3B+K4B;
				countRK<=countRK+1;
			
			elsif countRK=11 then
				K4A<=M1A*q3A + K4A;
				K4B<=M1C*q3A + K4B;
				countRK<=countRK+1;
				
			elsif countRK=12 then
				rkAux0<=K1A + 2*K2A + 2*K3A + K4A;
				rxAux1<=K1B + 2*K2B + 2*K3B + K4B;
				rkAux2<=to_float(0.16666666666666666,rkAux2)*dt;
				rxAux3<=to_float(0.16666666666666666,rxAux3)*dt;
				countRK<=countRK+1;
				
			elsif countRK=13 then
				v1<=v1+rkAux0*rkAux2;
				v2<=v2+rxAux1*rxAux3;
				countRK<=countRK+1;
			
			elsif countRK=14 then
				rk_flag<='1';
				countRK<=countRK+1;
				
			elsif countRK=15 then
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
	
	
end WMM_arch;