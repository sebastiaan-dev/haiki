export interface Article {
  title: string;
  sections: {
    h1?: string;
    h2?: string;
    p: string[];
  }[];
}
