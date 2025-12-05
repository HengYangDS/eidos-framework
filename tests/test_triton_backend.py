import unittest
from eidos import Source, Map, Sink
from eidos.zero.compiler import Compiler

class TestTritonBackend(unittest.TestCase):
    def test_triton_codegen(self):
        """
        Verifies that the Triton backend generates valid Python code containing @triton.jit kernels.
        """
        print("\n--- Testing Triton (GPU) Backend ---")
        
        flow = (
            Source("s3://vectors.parquet")
            >> Map(lambda x: x * 2)
            >> Sink("cuda://output")
        )
        
        graph = flow.compile()
        
        # Compile to GPU Kernel (Source Code)
        kernel_src = Compiler.compile(graph, target="triton")
        
        # Since we have 3 nodes (Source -> Map -> Sink), the compiler returns a list of results
        # The Map node result should contain the kernel code.
        
        # We expect: [SourceStr, KernelStr, SinkStr]
        print(f"Compilation Result Type: {type(kernel_src)}")
        
        # Flatten result if needed (Transpiler returns list for DAG)
        results = kernel_src if isinstance(kernel_src, list) else [kernel_src]
        
        kernel_found = False
        for code in results:
            if "import triton" in str(code):
                kernel_found = True
                print("Found Triton Kernel:")
                print("\n".join(str(code).split("\n")[:6])) # Print header
                self.assertIn("@triton.jit", code)
                self.assertIn("def lambda_kernel", code)
        
        self.assertTrue(kernel_found, "Triton kernel code was not generated")
        print("--- Triton Backend OK ---")

if __name__ == "__main__":
    unittest.main()
