import React from 'react';
import { Button } from "../ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

const Refinements = ({ onRefine }) => {
  return (
    <Card className="refinements-section mt-4">
      <CardHeader>
        <CardTitle>Refine Content</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-wrap gap-2">
        <Button onClick={() => onRefine('shorten')} variant="outline">Shorten</Button>
        <Button onClick={() => onRefine('changeTone')} variant="outline">Change Tone</Button>
      </CardContent>
    </Card>
  );
};

export default Refinements;

