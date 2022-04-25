export interface Comment {
  body: string;
  created: string;
  score: string;
  permalink: string;
  url?: string;
  prediction: number;
  thread_id: number;
  id: number;
  author?: string;
}

export type SeriesData = {
  x: string;
  y: [number, number, number, number];
};

export type SeriesLinearData = {
  x: string;
  y: number;
};

export type Chart = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}


export type DataChart = {
  series: [SeriesData];
  linear: [SeriesLinearData];
};
