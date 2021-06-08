% data from ./result/result_total.json
title = {'among us', 'apex lengend', ...
'fortnite', 'minecraft', 'overwatch', 'mario odyssey', 'botw', ...
 'roblox'};
x = [0.5420;0.3333;0.6222;0.4337;0.5053;0.2967;0.3604;0.58];
b = bar(x);

% set value on top of the bar
xtip = b.XEndPoints;
ytip = b.YEndPoints;
lable = string(b.YData);
text(xtip, ytip, lable, 'HorizontalAlignment','center',...
    'VerticalAlignment','bottom');

% set xlabel & ylabel
ylabel('clickbait per video');
set(gca, 'xticklabel', title);

% change color of the bar
b.FaceColor = 'flat';
b.CData(1,:) = [0.5 0 0];
b.CData(2,:) = [1 1 0];
b.CData(3,:) = [1 0 0.5];
b.CData(4,:) = [0 0.5 0.5];
b.CData(5,:) = [1 0.5 0.5];
b.CData(6,:) = [0.5 1 1];
b.CData(7,:) = [0 0 0.5];
b.CData(8,:) = [1 0 1];

