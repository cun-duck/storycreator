def split_story_into_scenes(full_story, num_scenes=10):
    words = full_story.split()
    words_per_scene = len(words) // num_scenes
    
    scenes = []
    for i in range(num_scenes):
        start = i * words_per_scene
        end = (i + 1) * words_per_scene if i < num_scenes - 1 else None
        scene = " ".join(words[start:end])
        scenes.append(scene.strip())
    
    return scenes
