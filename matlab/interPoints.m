clc;
clear all;

%% load files
%filename='../data/interPointsTest/sec600000c.jpg';
%I1 = imread(filename);

 points = [
     [41.058441558441416 146.33982683982674 251.62121212121212 348.5909090909091 426.16666666666674 489.8896103896104 578.5476190476192 ...
     656.1233766233768 805.7337662337663 855.6038961038964 916.5562770562774 974.7380952380954 1057.8549783549786 1124.3484848484852 ...
     1185.3008658008662 1249.0238095238099]
     [482.6861471861471 441.1277056277055 407.8809523809522 385.7164502164501 360.78138528138516 341.3874458874458 319.22294372294357 ...
     291.5173160173158 291.5173160173158 313.681818181818 330.3051948051947 346.9285714285712  360.78138528138516  366.3225108225107 ... 
     385.7164502164501 396.7987012987012]
     ]
 out1 = single(points(1,:)');
 out2 = single(points(2,:)');
%[out1,out2]=textread('../data/interPointsTest/sec600000c.txt','%d%d'); 
  
interpOut1=[];
interpOut2=[];

%% interpret points
 for i=1:size(out1,1)-1
    xIndex1=out1(i);
    yIndex1=out2(i);
    xIndex2=out1(i+1);
    yIndex2=out2(i+1);
    
    interpOut1=[interpOut1 xIndex1];
    interpOut2=[interpOut2 yIndex1];
    
    if(xIndex2~=xIndex1||yIndex2~=yIndex1)
    
    if(xIndex2>xIndex1)
        tmpX=[xIndex1 xIndex2];
        tmpY=[yIndex1 yIndex2];
        xIndex3=xIndex1:1:xIndex2;
        yIndex3=interp1(tmpX,tmpY,xIndex3);
    end
        
    if(xIndex2<xIndex1)
        tmpX=[xIndex1 xIndex2];
        tmpY=[yIndex1 yIndex2];
        xIndex3=xIndex1:-1:xIndex2;
        yIndex3=interp1(tmpX,tmpY,xIndex3);
    end
    
    if(xIndex2==xIndex1&&yIndex2>=yIndex1)
        tmpX=[xIndex1 xIndex2];
        tmpY=[yIndex1 yIndex2];
        
        yIndex3=yIndex1:1:yIndex2;
        xIndex3=interp1(tmpY,tmpX,yIndex3);
    end
    
    if(xIndex2==xIndex1&&yIndex2<yIndex1)
        tmpX=[xIndex1 xIndex2];
        tmpY=[yIndex1 yIndex2];
        
        yIndex3=yIndex1:-1:yIndex2;
        xIndex3=interp1(tmpY,tmpX,yIndex3);
    end
    xIndex3=round(xIndex3);
    yIndex3=round(yIndex3);
    t1=size(xIndex3,2);
    t2=size(yIndex3,2);
    
    if(t1>2)
    xIndex4=xIndex3(2:t1-1);
    yIndex4=yIndex3(2:t2-1);  
    interpOut1=[interpOut1 xIndex4];
    interpOut2=[interpOut2 yIndex4];
    end
    end
 end
 
%% caculate loss
 points2 = [
     [43 142 250 340 424 484 572 ...
     658 803 855 914 974 1056 1122 ...
     1162 1249]
     [471 455 402 381 366 348 317 ...
     298 298 318 330 346  366  367 ... 
     381 392]
     ]
loss = 0;
for point = points2
    distance = sqrt((interpOut1 - point(1)).^2 + (interpOut2 - point(2)).^2);
    loss = loss + min(distance);
end
disp(loss);

%% plot
%imshow(I1);hold on;
plot(interpOut1,interpOut2,'g.');hold on;
plot(points2(1,:),points2(2,:),'r.', 'MarkerSize', 20);hold on;
plot(points(1,:),points(2,:),'b.', 'MarkerSize', 20);hold on;
grid on;
xlabel('ºá×ø±ê(pixel)');
ylabel('×Ý×ø±ê(pixel)');
set(gca,'YDir','reverse');
print(gcf,'-dpng','result.png');
disp('----------------------->ok');