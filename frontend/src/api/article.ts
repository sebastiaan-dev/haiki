import { BASE_URL } from "@/constants";
import {
  ArticelTitelsDTO,
  articleSchema,
  articleTitelsDTOSchema,
} from "@/types/article";
import { skipToken, useQuery } from "@tanstack/react-query";
import axios from "axios";
import json2md from "json2md";

const getArticleTitles = async (topic: string): Promise<ArticelTitelsDTO> => {
  const response = await axios.get(`${BASE_URL}/articles/${topic}`);

  return articleTitelsDTOSchema.parse(response.data);
};

export const useArticleTitles = (topic?: string) => {
  return useQuery({
    queryKey: ["articleTitles"],
    queryFn: topic ? () => getArticleTitles(topic) : skipToken,
  });
};

const getArticle = async (
  topic: string,
  articleId: string,
  markdown: boolean
): Promise<any> => {
  const response = await axios.get(`${BASE_URL}/article/${topic}/${articleId}`);

  const data = articleSchema.parse(response.data);

  if (!markdown) {
    return data;
  }

  const mdString = data.sections.reduce(
    (acc, section) => acc.concat(json2md(section)),
    ""
  );
  return mdString;
};

export const useArticle = (
  topic: string,
  articleId: string,
  markdown = true
) => {
  return useQuery({
    queryKey: ["articleData", markdown],
    queryFn: () => getArticle(topic, articleId, markdown),
  });
};
