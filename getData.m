%function data = getData(path)

% read all filename in dir
img_path = './data/image/';
anno_path = './data/';

dirs = dir([img_path,'*.jpg']);
dircell = struct2cell(dirs)';
imgnames = dircell(:,1);
filename, annoname = cell(size(imgnames));

% get image names & xml file names
for i = 1:size(imgnames)
    file_name = char(imgnames(i));
    k = find('.'== file_name);
    filename{i} = file_name(1:k-1);%remove suffix
    annoname{i} = [filename{i},'.xml'];%add suffix
end

