function write_dada_file (file_id, data, header, verbose_)
  % Write a DADA file
  % @method write_dada_file
  % @param {double} file_id - The DADA file's file id as generated by `fopen`
  % @param {single/double []} data - The data to be written to the DADA file
  % @param {containers.Map} header - The DADA header written to the DADA file

  % make sure that the data characterisitcs in the header are correct
  verbose = 0;
  if exist('verbose_', 'var')
    verbose = verbose_;
  end

  dtype = class(data);

  header('NBIT') = '64';
  if class(data) == 'single'
    header('NBIT') = '32';
  end

  header('NDIM') = '2';
  if isreal(data)
    header('NDIM') = '1';
  end

  size_data = size(data);
  header('NPOL') = num2str(size_data(1));
  header('NCHAN') = num2str(size_data(2));

  % ensure we're at the start of the file
  frewind(file_id);
  write_header(file_id, header);

  if verbose
    fprintf('write_data_file: dtype=%s\n', class(data));
  end
  
  if ~isreal(data)
    n_pol = size_data(1);
    n_chan = size_data(2);
    n_dat = size_data(3);
    temp = zeros(2*n_pol, n_chan, n_dat, dtype);
    for i_pol=1:n_pol
      temp(2*(i_pol-1) + 1, :, :) = real(data(i_pol, :, :));
      temp(2*(i_pol-1) + 2, :, :) = imag(data(i_pol, :, :));
    end
    data = temp;
  end
  fwrite(file_id, reshape(data, numel(data), 1), dtype);
end
