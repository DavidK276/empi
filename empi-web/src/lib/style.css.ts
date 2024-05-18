import { style } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const row = style({
	display: 'flex',
	flexDirection: 'row',
	gap: vars.md,
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
	gap: vars.md,
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
	color: vars.danger,
	display: 'block',
	margin: `${vars.sm} 0`
});

export const box = style({
	border: '1px solid gray',
	borderRadius: vars.xs,
	boxShadow: '0 0 4px gray',
	margin: `${vars.sm} 0`,
	padding: `${vars.sm} ${vars.lg}`
});