export function formatDuration(seconds: number): string {
	const minutes = Math.floor(seconds / 60)
	const remainingSeconds = seconds % 60
	return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

export function getThumbnailSrc(
	thumbnail: string | null,
	defaultThumbnail = '/thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png'
): string {
	return thumbnail || defaultThumbnail
}
