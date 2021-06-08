% data from ./result/result_total.json
clickBaitNum = 1190;
nonClickBaitNum = 2623;

x = [clickBaitNum nonClickBaitNum];
label={'clickbait','non clickbait'};
pie(x, label);