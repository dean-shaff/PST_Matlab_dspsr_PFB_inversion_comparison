function data_header = read_dada_file (file_id, verbose_)
  % Read from a DADA file, given some file_id
  % @method read_dada_file
  % @param {double} file_id - The DADA file's file id as generated by `fopen`
  % @return {cell array} - cell array containing the data and header.
  verbose = 0;
  if exist('verbose_', 'var')
    verbose = verbose_;
  end


  hdr_map = read_header(file_id);
  n_dim = str2num(hdr_map('NDIM'));
  n_pol = str2num(hdr_map('NPOL'));
  n_bit = str2num(hdr_map('NBIT'));
  n_chan = str2num(hdr_map('NCHAN'));
  dtype = 'single';
  if n_bit == 64
    dtype = 'double';
  end

  if verbose
    fprintf('read_dada_file: dtype=%s\n', dtype);
  end
  % ensure that we're reading only the data we want
  hdr_size = str2num(hdr_map('HDR_SIZE'));
  frewind(file_id);
  % `fread` reads sequentially, so we'll advance the file by hdr_size bytes
  % before reading the actual data buffer.
  fread(file_id, hdr_size, 'uint8');
  data = fread(file_id, dtype);
  data = reshape(data, 1, []);
  if n_dim == 2
    data = reshape(data, n_pol*n_dim, n_chan, []);
    data_size = size(data);
    n_dat = data_size(end);
    dat_temp = complex(zeros(n_pol, n_chan, n_dat, dtype));

    for i_pol=1:n_pol
      idx = 2*i_pol - 1;
      dat_temp(i_pol, :, :) = squeeze(complex(data(idx, :, :), data(idx+1, :, :)));
    end
    data = dat_temp;
  else
    data = reshape(data, n_pol, n_chan, []);
  end
  data_header = {data, hdr_map};
end
