import heapq
import os

def external_sort(input_file, output_file, mem_limit=4*1024*1024):  
    chunk_size = 100000  
    temp_files = []
    
    #  Create sorted runs
    with open(input_file, 'r') as f:
        while True:
            chunk = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line: break
                chunk.append(int(line.strip()))
            if not chunk: break
            chunk.sort()
            temp = f'temp_{len(temp_files)}.txt'
            with open(temp, 'w') as t:
                for num in chunk:
                    t.write(f'{num}\n')
            temp_files.append(temp)
    
    #  Merge
    with open(output_file, 'w') as out:
        heap = []
        file_handles = [open(tf, 'r') for tf in temp_files]
        for i, fh in enumerate(file_handles):
            line = fh.readline()
            if line:
                heapq.heappush(heap, (int(line.strip()), i))
        
        while heap:
            val, idx = heapq.heappop(heap)
            out.write(f'{val}\n')
            line = file_handles[idx].readline()
            if line:
                heapq.heappush(heap, (int(line.strip()), idx))
        
        for fh in file_handles:
            fh.close()
    
    # Cleanup
    for tf in temp_files:
        os.remove(tf)

# Usage
external_sort('large_file.txt', 'sorted.txt')
