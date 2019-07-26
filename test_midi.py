import mido

if __name__ == "__main__":
	mid1 = mido.MidiFile('midi/sample1-1.mid')
	mid2 = mido.MidiFile('midi/sample1-2.mid')

	assert len(mid1.tracks[0]) == len(mid2.tracks[0])

	for i in range(len(mid1.tracks[0])):
		if not mid1.tracks[0][i].is_meta:
			mid1.tracks[0][i].time = mid2.tracks[0][i].time

	mid1.save('midi/sample1-3.mid')
