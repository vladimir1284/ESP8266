data = csvread('step-30.csv');
temp = data(:,2)';
u = data(:,7)';
[sysid, Gd] = arx(u, temp, 0, 2, 1, 10, 150);
t = 0:10:10*(size(temp)(2)-1);
plot(t,u);
hold on
lsim(Gd,u,t);