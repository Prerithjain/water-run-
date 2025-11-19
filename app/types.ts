export interface Person {
    id: number;
    name: string;
    score: number;
    last_visit: string | null;
}

export interface Run {
    id: number;
    timestamp: string;
    mode: 'alone' | 'group';
    actors: number[];
    actor_names: string[];
    points_each: number;
}

export interface StateResponse {
    people: Person[];
    total_runs: number;
}

export interface SuggestionResponse {
    suggested: Person[];
    reason: string;
}
