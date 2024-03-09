import { z } from "zod";

export const articleTopicDTOSchema = z.array(z.string());

export type ArticleTopicDTO = z.infer<typeof articleTopicDTOSchema>;

export const articleTitelsDTOSchema = z.array(z.string());

export type ArticelTitelsDTO = z.infer<typeof articleTitelsDTOSchema>;

export const sectionSchema = z.object({
  h1: z.string().optional(),
  h2: z.string().optional(),
  p: z.array(z.string()),
});

export const articleSchema = z.object({
  title: z.string(),
  sections: z.array(sectionSchema),
});

export type Article = z.infer<typeof articleSchema>;
