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
		return 'common.winter_semester';
	}
	return 'common.summer_semester';
}

export function getSettingQuery(settings: Setting[]) {
	const params = new URLSearchParams();
	params.set('year', getCurrentAcademicYear(settings));
	params.set('semester', getCurrentSemester(settings));
	return params.toString();
}
