import { BASE_URL } from "@/constants";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const getArticle = () =>
  axios.get(`${BASE_URL}/test/article`).then((res) => res.data);

export const useArticle = () => {
  return useQuery({
    queryKey: ["articleData"],
    queryFn: getArticle,
  });
};
