% data from ./result/result_total.json
clickBaitAvgViews = 2884339;
non_clickBaitAvgViews = 5346728;

x = [clickBaitAvgViews; non_clickBaitAvgViews];
b = bar(x,'stack');

% set value on top of the bar
xtip = b.XEndPoints;
ytip = b.YEndPoints;
lable = string(b.YData);
text(xtip, ytip, lable, 'HorizontalAlignment','center',...
    'VerticalAlignment','bottom');

% set xlabel & ylabel
ylabel('avg views');
set(gca, 'xticklabel', {'clickbait', 'non clickbait'});

% change color of the bar
b.FaceColor = 'flat';
b.CData(1,:) = [1 0 0];
