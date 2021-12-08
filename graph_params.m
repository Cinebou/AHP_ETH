log_852718 = readtable("log_paramter852718.csv");
log_903010 = readtable("log_paramter903010.csv");
log_2temp_852718 = readtable("log_paramter_2temp_852718.csv");
log_2temp_903010 = readtable("log_parameter_2temp_903010.csv");

mv_fig = figure(1);
plot(log_852718{:,'t'},log_852718{:,'mv'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'mv'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'mv'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'mv'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('m_v [kg_{water}/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off

h_back_sor = figure(2);
plot(log_852718{:,'t'},log_852718{:,'h_sor'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'h_sor'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'h_sor'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'h_sor'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('h_{sor} [J/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off

h_back_water = figure(3);
plot(log_852718{:,'t'},log_852718{:,'h_ad_water'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'h_ad_water'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'h_ad_water'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'h_ad_water'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('h_{ad.water} [J/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off

h_back_hx = figure(4);
plot(log_852718{:,'t'},log_852718{:,'h_hx'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'h_hx'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'h_hx'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'h_hx'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('h_{hx} [J/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off

h_v_from_evp = figure(5);
plot(log_852718{:,'t'},log_852718{:,'h_v_from_evp'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'h_v_from_evp'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'h_v_from_evp'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'h_v_from_evp'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('h_{v.evp} [J/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off

h_v_to_cond = figure(6);
plot(log_852718{:,'t'},log_852718{:,'h_v_to_cond'},'--ro','linewidth',1.5,'DisplayName','852718');
hold on
plot(log_903010{:,'t'},log_903010{:,'h_v_to_cond'},'--bo','linewidth',1.5,'DisplayName','903010');
hold on
plot(log_2temp_852718{:,'t'},log_2temp_852718{:,'h_v_to_cond'},'--go','linewidth',1.5,'DisplayName','852718_{2temp}');
hold on
plot(log_2temp_903010{:,'t'},log_2temp_903010{:,'h_v_to_cond'},'--yo','linewidth',1.5,'DisplayName','903010_{2temp}');
legend
xlabel('t_{cycle} [sec]');
ylabel('h_{v.cond} [J/sec]');
set(gca,'FontSize',20,'FontName','Times New Roman');
pbaspect([15 15 15]);
hold off
