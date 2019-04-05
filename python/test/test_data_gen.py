import unittest
import logging
import os

import numpy as np

from data_gen import generate_test_vector


class TestDataGen(unittest.TestCase):

    time_domain_args = ("time", 1000, 0.1, 1)
    time_domain_kwargs = dict(n_pol=2,
                              output_dir="./",
                              output_file_name="time_domain_impulse.dump",
                              dtype=np.complex64)

    freq_domain_args = ("freq", 1000, 0.1, np.pi/4, 0.1)
    freq_domain_kwargs = dict(n_pol=2,
                              output_dir="./",
                              output_file_name="complex_sinusoid.dump",
                              dtype=np.complex64)

    @classmethod
    def setUpClass(cls):
        cls.file_paths = [
            cls.freq_domain_kwargs["output_file_name"],
            cls.time_domain_kwargs["output_file_name"]
        ]

    def test_generate_test_vectors_matlab(self):
        generator = generate_test_vector(backend="matlab")
        dada_file = generator(*self.time_domain_args,
                              **self.time_domain_kwargs)
        self.assertTrue(self.time_domain_kwargs["output_file_name"]
                        in dada_file.file_path)
        dada_file = generator(*self.freq_domain_args,
                              **self.freq_domain_kwargs)
        self.assertTrue(self.freq_domain_kwargs["output_file_name"]
                        in dada_file.file_path)

    def test_generate_test_vectors_python(self):
        generator = generate_test_vector(backend="python")
        dada_file = generator(*self.time_domain_args,
                              **self.time_domain_kwargs)
        self.assertTrue(self.time_domain_kwargs["output_file_name"]
                        in dada_file.file_path)

        dada_file = generator(*self.freq_domain_args,
                              **self.freq_domain_kwargs)

        self.assertTrue(self.freq_domain_kwargs["output_file_name"]
                        in dada_file.file_path)

    def test_generate_test_vectors_default_name(self):
        original_val = self.time_domain_kwargs["output_file_name"]

        self.time_domain_kwargs["output_file_name"] = None
        generator = generate_test_vector(backend="python")
        dada_file = generator(*self.time_domain_args,
                              **self.time_domain_kwargs)
        expected_file_name = ("time_domain_impulse.1000."
                              "0.100-1.000.2.single.python.dump")

        self.assertTrue((os.path.basename(dada_file.file_path) ==
                         expected_file_name))

        self.time_domain_kwargs["output_file_name"] = original_val
        self.__class__.file_paths.append(dada_file.file_path)

    @classmethod
    def tearDownClass(cls):

        for file_path in cls.file_paths:
            os.remove(file_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
