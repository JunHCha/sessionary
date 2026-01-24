export interface PendingAction {
	type: string
	sessionId?: number
}

const PENDING_ACTION_KEY = 'pendingAction'

export function savePendingAction(action: PendingAction): void {
	if (typeof sessionStorage !== 'undefined') {
		sessionStorage.setItem(PENDING_ACTION_KEY, JSON.stringify(action))
	}
}

export function getPendingAction(): PendingAction | null {
	if (typeof sessionStorage === 'undefined') {
		return null
	}

	const stored = sessionStorage.getItem(PENDING_ACTION_KEY)
	if (!stored) {
		return null
	}

	sessionStorage.removeItem(PENDING_ACTION_KEY)
	return JSON.parse(stored)
}
