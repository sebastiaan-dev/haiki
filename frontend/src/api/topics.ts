import { BASE_URL } from "@/constants";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const getTopics = (): Promise<string[]> => {
  const data = axios.get(`${BASE_URL}/topics`).then((res) => res.data);
  return data;
};

export const useTopics = () => {
  return useQuery({
    queryKey: ["articleData"],
    queryFn: getTopics,
  });
};
