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
  const response = await axios.get(`${BASE_URL}/articles/${topic}/title`);

  return articleTitelsDTOSchema.parse(response.data);
};

export const useArticleTitles = (topic?: string) => {
  console.log("topic", topic);
  return useQuery({
    queryKey: ["articleTitles"],
    queryFn: topic ? () => getArticleTitles(topic.toLowerCase()) : skipToken,
  });
};

const getArticle = async (
  topic: string,
  articleId: string,
): Promise<string> => {
  const response = await axios.get(`${BASE_URL}/article/${topic}/${articleId}`);

  const data = articleSchema.parse(response.data);

  const mdString = data.sections.reduce(
    (acc, section) => acc.concat(json2md(section)),
    "",
  );
  return mdString;
};

export const useArticle = (topic?: string, articleId?: string) => {
  console.log(topic, articleId);
  const canQuesry = topic && articleId;
  return useQuery({
    queryKey: ["articleData"],
    queryFn: canQuesry ? () => getArticle(topic, articleId) : skipToken,
  });
};
