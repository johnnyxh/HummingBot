export function getTimeUnitRepresentation(number) {
	let s = String(number)
	while (s.length < 2) {
		s = '0' + s;
	}
	return s;
} 

export function getTimestamp(timestamp) {
	const hours = Math.trunc(timestamp / 3600);
	const minutes = Math.trunc((timestamp % 3600) / 60);
	const seconds = (timestamp % 3600) % 60;
	return `${getTimeUnitRepresentation(hours)}:${getTimeUnitRepresentation(minutes)}:${getTimeUnitRepresentation(seconds)}`;
}