% data from ./result/result_total.json
title = {'among us', 'apex lengend', ...
'fortnite', 'minecraft', 'overwatch', 'mario odyssey', 'botw', ...
 'roblox'};
x = [4709388 3141769;220452 558823;840028 608186;2005095 3826873;2108982 99738;3345401 6178647;828265 804702;433979 578584];
b = bar(x);

% % set value on top of the bar
% xtip = b.XEndPoints;
% ytip = b.YEndPoints;
% lable = string(b.YData);
% text(xtip, ytip, lable, 'HorizontalAlignment','center',...
%     'VerticalAlignment','bottom');

% set xlabel & ylabel
ylabel('avg views');
xlabel('clickbait vs no clickbait');
set(gca, 'xticklabel', title);

% % change color of the bar
% b.FaceColor = 'flat';
% b.CData(1,:) = [0.5 0 0];
% b.CData(2,:) = [1 1 0];
% b.CData(3,:) = [1 0 0.5];
% b.CData(4,:) = [0 0.5 0.5];
% b.CData(5,:) = [1 0.5 0.5];
% b.CData(6,:) = [0.5 1 1];
% b.CData(7,:) = [0 0 0.5];
% b.CData(8,:) = [1 0 1];