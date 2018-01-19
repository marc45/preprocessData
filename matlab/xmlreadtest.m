% parase xml DOM nodes into struct array 
% function theStruct =  xml2Struct(file_path, file_name)
clear;clc

% read xml file
file_path = '../';
file_name = 'test.xml';
try
    xDoc = xmlread([file_path,file_name]);
catch
    error('Failed to read XML file %s.',file_name);
end

disp('loading...');

annotation = xDoc.getElementsByTagName('annotation');
annotation = annotation.item(0);
scaleNode = annotation.getElementsByTagName('scale').item(0);
scale = str2num(char(scaleNode.getTextContent()));
typeNode = annotation.getElementsByTagName('type').item(0);
type = char(typeNode.getTextContent());
pointsNode = annotation.getElementsByTagName('points');
points = cell(1,1);
for i = 0:pointsNode.getLength-1
    pointNode = pointsNode.item(i);
    idText = pointNode.getElementsByTagName('id').item(0).getTextContent();
    id = str2num(char(idText));
    xaxis = char(pointNode.getElementsByTagName('xaxis').item(0).getTextContent());
    yaxis = char(pointNode.getElementsByTagName('yaxis').item(0).getTextContent());
    points{1,i+1} = struct('id',id,'x',xaxis,'y',yaxis);
end

annoroad = struct('type',type,'scale',scale,'points',points);
annolist = struct('image_name',file_name,'annoroad',annoroad);

% put all data into struct data
data = struct('annolist',annolist);

save('test.mat','data');
disp('Success!');
