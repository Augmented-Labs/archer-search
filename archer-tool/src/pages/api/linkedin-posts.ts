// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "POST") {
    const searchType = req.body.searchType;
    const url = req.body.url;
    const query = req.body.query;

    const results = await axios.post("http://127.0.0.1:8000/relevancy", {
      url,
      query,
      searchType,
    });
    return res.status(200).json(results.data);
  } else {
    return res.status(400).json({ error: "Method not allowed" });
  }
}
