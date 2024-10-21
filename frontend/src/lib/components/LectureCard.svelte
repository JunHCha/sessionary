<script lang="ts">
	import type { LectureList as LectureInList } from '$lib/client'

	export let lecture: LectureInList
</script>

<div class="lecture-card">
	<img src="{lecture.title}" alt="{lecture.title}" />
	<h3>{lecture.description}</h3>
	<p>{lecture.length_sec}초</p>
</div>

<style>
	.lecture-card {
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		padding: 1rem;
		margin: 0.5rem;
		width: 200px;
	}

	img {
		width: 100%;
		height: 120px;
		object-fit: cover;
		border-radius: 4px;
	}

	h3 {
		margin: 0.5rem 0;
		font-size: 1rem;
	}

	p {
		font-size: 0.8rem;
		color: #666;
	}
</style>
