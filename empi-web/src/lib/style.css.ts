import { style } from '@vanilla-extract/css';

export const row = style({
	display: 'flex',
	flexDirection: 'row',
	gap: 'var(--md)',
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	},
	'@media': {
		'screen and (max-width: 768px)': {
			selectors: {
				'.m-col&': {
					flexDirection: 'column'
				}
			}
		}
	}
});

export const col = style({
	display: 'flex',
	flexDirection: 'column',
	gap: 'var(--md)',
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	}
});

export const content = style({
	maxWidth: 1280,
	width: '100%'
});

export const error = style({
	color: 'var(--danger)',
	display: 'block',
	margin: 'var(--sm) 0'
});

export const box = style({
	border: '1px solid gray',
	borderRadius: 'var(--xs)',
	boxShadow: '0 0 4px gray',
	margin: 'var(--sm) 0',
	padding: 'var(--sm) var(--lg)'
});

export const message = style({
	display: "inline-flex",
	alignItems: "center",
	margin: 0
});