import { create } from "zustand";

interface ArticleState {
  topic?: string; // Supliments or Health or Bussiness
  title?: string; // Matcha Creatine ect.
  articleMarkdown?: string;

  setTopic: (topic: string) => void;
  setTitle: (title: string) => void;
  setArticleMarkdown: (markdown: string) => void;
}
export const useArticleStore = create<ArticleState>((set) => ({
  topic: undefined,
  title: undefined,
  articleMarkdown: undefined,

  setTopic: (topic) => set({ topic }),
  setTitle: (title) => set({ title }),
  setArticleMarkdown: (markdown) => set({ articleMarkdown: markdown }),
}));
