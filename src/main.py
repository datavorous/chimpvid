from chimp.worker import Worker

worker = Worker(
    workspace="Pointers",
    topic="Write a playful and educational rhyming song for kids about memory pointers in programming. The song should introduce concepts like addresses, referencing, dereferencing, and avoiding null pointers in a simple and fun way. Simple 10 line song. Just provide the text.",
    num_lines=10,  
    style="Vintage Anime like that of Ghibli Studios from the 90s"  
)

worker.process()
worker.create_vid(output_path="pointers.mp4", fps=10)
worker.flush()
