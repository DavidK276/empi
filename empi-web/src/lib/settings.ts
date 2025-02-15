import { getSetting } from "$lib/functions";
import type { Setting } from "$lib/objects/Setting";

export function getCurrentAcademicYear(settings: Setting[]) {
	return getSetting(settings, "CURRENT_ACAD_YEAR") ?? "2024/2025";
}

export function getCurrentSemester(settings: Setting[]) {
	return getSetting(settings, "CURRENT_SEMESTER") ?? "Z";
}

export function getCurrentSemesterUI(settings: Setting[]) {
	const currentSemester = getCurrentSemester(settings);
	if (currentSemester === 'Z') {
		return "Zimný";
	}
	return "Letný";
}