function test_synthesize ()
  input_file_path = './../data/polyphase_analysis.complex_sinusoid.dump';
  output_file_name = 'polyphase_synthesis.complex_sinusoid.dump';
  output_dir = './';
  synthesize(...
    input_file_path,...
    '1024',...
    output_file_name,...
    output_dir,...
    '1',... % verbose
    '1',... % sample_offset
    '1',... % deripple
    '128',... % overlap
    'tukey'...
  )
  output_file_path = fullfile(output_dir, output_file_name);
  delete(output_file_path);
end
