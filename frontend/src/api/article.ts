import { testData } from "@/assets/test-data";
import { Article } from "@/types/article";
import { useQuery } from "@tanstack/react-query";
import json2md from "json2md";

const getArticle = async (): Promise<string> => {
  // const data = axios.get(`${BASE_URL}/test/article`).then((res) => res.data);
  const data = await new Promise<Article>((resolve) => resolve(testData));

  const mdString = data.sections.reduce(
    (acc, section) => acc.concat(json2md(section)),
    "",
  );
  return mdString;
};

export const useArticle = () => {
  return useQuery({
    queryKey: ["articleData"],
    queryFn: getArticle,
  });
};
