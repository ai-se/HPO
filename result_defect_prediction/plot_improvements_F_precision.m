clf
 FigHandle = figure('Position', [220, 300, 200, 400]);
%plot([1:17],[0:0])
x = [1:17]
box on 
hold on
plot(x,[-19.0, -19.0, -11.0, -7.0, -6.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 4.0, 4.0, 7.0, 73.0, 91.0], '-r*')
hold on
plot(x,[-17.0, -1.0, 1.0, 2.0, 2.0, 4.0, 4.0, 4.0, 6.0, 8.0, 9.0, 11.0, 15.0, 18.0, 19.0, 29.0, 57.0],'-b+')
hold on
plot(x,[-20.0, -12.0, -10.0, -4.0, -4.0, -1.0, -1.0, 0.0, 1.0, 5.0, 6.0, 6.0, 15.0, 18.0, 22.0, 27.0, 59.0], '-gx')
axis([1 17 -100 100])
legend('WHERE','CART','R.Forest','Location','South')
set(gca,'XTick', [1,4,8,12,17])
set(gca, 'YTick',[-50,0,50,100])
hline = refline([0 0]);
set(hline,'Color','k')
title('F')
legend('boxoff')
xlabel('improvements, sorted')

 FigHandle = figure('Position', [220, 300, 200, 400]);
%plot([1:17],[0:0])
x = [1:17]
box on 
hold on
plot(x,[-30.0, -26.0, -25.0, 0.0, 0.0, 0.0, 6.0, 9.0, 13.0, 15.0, 42.0, 59.0, 59.0, 63.0, 72.0, 73.0, 96.0], '-r*')
hold on
plot(x,[-23.0, -4.0, 3.0, 3.0, 4.0, 5.0, 8.0, 8.0, 12.0, 15.0, 16.0, 29.0, 33.0, 34.0, 38.0, 59.0, 62.0],'-b+')
hold on
plot(x,[-23.0, -1.0, 0.0, 1.0, 1.0, 5.0, 6.0, 6.0, 8.0, 9.0, 10.0, 18.0, 28.0, 33.0, 35.0, 36.0, 61.0], '-gx')
axis([1 17 -100 100])
legend('WHERE','CART','R.Forest','Location','South')
set(gca,'XTick', [1,4,8,12,17])
set(gca, 'YTick',[-50,0,50,100])
hline = refline([0 0]);
set(hline,'Color','k')
title('precision')
legend('boxoff')
xlabel('improvements, sorted')