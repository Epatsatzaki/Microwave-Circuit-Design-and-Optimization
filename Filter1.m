function S = Filter1(p)
    % p = [Z01, Z02, Z0s1, Z0s2, Z0s3]
    Z01 = p(1); Z02 = p(2); Z0s1 = p(3); Z0s2 = p(4); Z0s3 = p(5);
    f0 = 1e9; Z0_sys = 50;
    
    % Frequency range for optimization (0 to 2 GHz)
    f = 0.01e9:0.01e9:2e9; 
    N = length(f);
    betaL = (pi/4) .* (f./f0); 
    
    % ABCD Matrices calculation (Stable method)
    M_line = @(Z0, th) [cos(th), 1j*Z0*sin(th); 1j*sin(th)/Z0, cos(th)];
    M_stub = @(Z0, th) [1, 0; 1j*tan(th)/Z0, 1];
    
    S11_abs = zeros(1, N);
    
    for k = 1:N
        th = betaL(k);
        % Total Transfer Matrix (Layout order)
        T = M_stub(Z0s1,th)*M_line(Z01,th)*M_stub(Z0s2,th)*M_line(Z02,th)*...
            M_stub(Z0s3,th)*M_line(Z02,th)*M_stub(Z0s2,th)*M_line(Z01,th)*...
            M_stub(Z0s1,th);
            
        A = T(1,1); B = T(1,2); C = T(2,1); D = T(2,2);
        S11 = (A + B/Z0_sys - C*Z0_sys - D) / (A + B/Z0_sys + C*Z0_sys + D);
        S11_abs(k) = abs(S11);
    end
    
    % Split into Passband (0-1 GHz) and Stopband (1-2 GHz)
    S11_pass = S11_abs(1:N/2);
    S11_stop = S11_abs(N/2+1:end);
    
    % Fitness Function #2: 
    % Minimize mean reflection in passband + Distance from 1.0 in stopband
    S = mean(S11_pass) + (1 - mean(S11_stop));
    
    % Ensure S is a real double scalar
    S = real(double(S));
end