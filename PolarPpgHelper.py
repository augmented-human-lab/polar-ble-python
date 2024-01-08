import csv
import math
import time
import datetime

CHANNEL_COUNT = 4
SAMPLE_RATE = 55

class PolarDataHandler:

    def __init__(self, file_path="polar_data.csv"):
        self.file_path = file_path
        self.initialize_csv_file()

    def initialize_csv_file(self):
        with open(self.file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ppg0", "ppg1", "ppg2", "ambient", "timestamp"])

    def control_point_handler(self, _, data):
        control_point_response = ', '.join('{:02x}'.format(x) for x in data)
        print(control_point_response)

    def hr_data_handler(self, _, data):
        print(int.from_bytes(data, byteorder='big', signed=False))

    def ppg_data_handler(self, _, data):
        ppg_references = [self.unpack_reference_ppg(data[i:i+3]) for i in range(10, 22, 3)]
        ppg_deltas = self.extract_ppg_deltas(data[22:])

        epoch_time = datetime.datetime.fromtimestamp(int(time.time()))
        time_list = [
            int((epoch_time + datetime.timedelta(seconds=i / SAMPLE_RATE)).timestamp() * 1e6) 
            for i in range(len(ppg_deltas) // CHANNEL_COUNT)
        ]

        ppg_values = []

        for i in range(0, len(ppg_deltas), CHANNEL_COUNT):
            ppg_sample = [delta + reference for delta, reference in zip(ppg_deltas[i:i+CHANNEL_COUNT], ppg_references)]
            ppg_references = ppg_sample
            ppg_sample += [time_list[i // CHANNEL_COUNT]]
            ppg_values += [ppg_sample]

        self.write_rows_to_csv(ppg_values)

    def extract_ppg_deltas(self, data):
        i = 0
        ppg_deltas = []

        while i < len(data):
            sample_size, sample_count = data[i:i+2]
            i += 2
            package_length = math.ceil(sample_size * sample_count * CHANNEL_COUNT / 8)
            ppg_deltas += self.unpack_ppg_deltas(data[i:i+package_length], sample_size)
            i += package_length

        return ppg_deltas

    def write_rows_to_csv(self, rows):
        with open(self.file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    def unpack_reference_ppg(self, data):
        raw_ppg = data[0] | (data[1] << 8) | (data[2] << 16)
        sign_bit = raw_ppg & (1 << 23)
        return raw_ppg if not sign_bit else raw_ppg - (1 << 24)

    def unpack_ppg_deltas(self, data, sample_size):
        bits = [format(byte, '08b') for byte in data]
        bit_string = ''.join(bits)
        return self.break_string_into_chunks(bit_string, sample_size)

    def break_string_into_chunks(self, input_string, sample_size, chunk_size=8):
        chunks = [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]

        head = 0
        tail = chunk_size

        bits_read = 0
        delta_block = []
        delta_samples = []

        index = 0
        while index < len(chunks):
            chunk = chunks[index]

            if index == len(chunks) - 1:
                if not chunk:
                    break
                if bits_read > 0:
                    delta_block += [chunk[bits_read-sample_size:]]
                    chunks[index] = chunk[:bits_read-sample_size]
                    bits_read = 0
                else:
                    delta_block = [chunk[:sample_size]]
                    chunks[index] = chunk[sample_size:]
                delta_samples += [self.parse_chunks(delta_block, sample_size)]
                delta_block = []
                continue

            if sample_size < chunk_size and tail - head > sample_size:
                delta_samples += [self.parse_chunks(chunk[head:sample_size], sample_size)]
                chunks[index] = chunk[sample_size:tail]
                tail = tail - sample_size
                continue

            delta_block += [chunk[head:tail]]
            bits_read += len(chunk[head:tail])

            tail = head

            if tail == 0:
                index += 1
                tail = chunk_size
                new_head = chunk_size - (sample_size - bits_read)
                head = max(new_head, 0)

            if bits_read == sample_size:
                bits_read = 0
                head = 0
                delta_samples += [self.parse_chunks(delta_block, sample_size)]
                delta_block = []

        return delta_samples

    def parse_chunks(self, ppg_delta_bits, sample_size):
        reversed_ppg_chunks = ppg_delta_bits[::-1]
        reversed_ppg_bits = ''.join(''.join(map(str, inner_list)) for inner_list in reversed_ppg_chunks)
        ppg_integer = int(reversed_ppg_bits, 2)
        if reversed_ppg_bits[0] == '1':
            ppg_integer -= 1 << sample_size
        return ppg_integer
