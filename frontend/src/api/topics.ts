import { BASE_URL } from "@/constants";
import { useArticleStore } from "@/store";
import { ArticleTopicDTO, articleTopicDTOSchema } from "@/types/article";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const getTopics = async (): Promise<ArticleTopicDTO> => {
  const response = await axios.get(`${BASE_URL}/topics`);

  return articleTopicDTOSchema.parse(response.data);
};

export const useTopics = () => {
  return useQuery({
    queryKey: ["articleData"],
    queryFn: getTopics,
  });
};
