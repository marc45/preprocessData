%function img_anno()
%-------------------------------------------
clear;clc;

%% PATH
img_path = '../data/image/';
anno_path = '../data/annotation/';

%% show image
[example_xml, message] = fopen([anno_path, 'example.xml'],'r');
if example_xml == -1
    disp(message);
end
dirs = dir([img_path,'*.jpg']);
dircell = struct2cell(dirs)';
imgnames = dircell(:,1);
for i = 1:size(imgnames)
    file_name = char(imgnames(i));
    k = find('.'== file_name);
    name = file_name(1:k-1);%remove suffix
    disp(['add annotation to ',file_name]);
    save([anno_path,name,'.xml'],'example_xml');
    imtool([img_path, file_name]);holdOn;
end
