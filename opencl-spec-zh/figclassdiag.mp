%
% author:	Ni Qingliang
% date:		2011-02-11
%
input metauml;

% draw item asso
vardef itemAss(expr pA, angleDir, texContent)=
   if (angleDir = -90):
      item(iAssoc)(texContent)(obj.ne = pA);
   elseif (angleDir = 180):
      item(iAssoc)(texContent)(obj.se = pA);
   elseif (angleDir = 90):
      item(iAssoc)(texContent)(obj.se = pA);
   elseif (angleDir = 0):
      item(iAssoc)(texContent)(obj.sw = pA);
   else:
      errmessage("the angle is error");
   fi;
enddef;

% draw path and item asso
vardef pathItem(text iLink)(expr thePath)(expr texHead, texTail)=

   numeric headDir;
   numeric tailDir;

   LinkStructure.ls(thePath, iLink.widthA, iLink.widthB);
   drawLinkStructure(ls)(iLink);

   headDir = angle (direction 0 of thePath);
   tailDir = angle (-direction (length thePath) of thePath);

   itemAss(point 0 of thePath, headDir, texHead);
   itemAss(point (length thePath) of thePath, tailDir, texTail);
enddef;

% draw link vertical
vardef linkV(text iLink)(expr pA, untilY)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (xpart(pA), untilY);

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;

% draw link hor
vardef linkH(text iLink)(expr pA, untilX)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (untilX, ypart(pA));

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;

% draw link hor Manhattan
vardef linkHV(text iLink)(expr pA, pB)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (xpart(pB), ypart(pA)) -- pB;

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;

vardef linkVH(text iLink)(expr pA, pB)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (xpart(pA), ypart(pB)) -- pB;

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;

%edge point
vardef objEdgeTop(suffix objA)(expr position)=
   position[objA.nw,objA.ne]
enddef;
vardef objEdgeBottom(suffix objA)(expr position)=
   position[objA.sw,objA.se]
enddef;
vardef objEdgeLeft(suffix objA)(expr position)=
   position[objA.nw,objA.sw]
enddef;
vardef objEdgeRight(suffix objA)(expr position)=
   position[objA.ne,objA.se]
enddef;

vardef linkVHV(text iLink)(expr pA, intY, pB)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (xpart(pA), intY) -- (xpart(pB), intY) -- pB;

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;
vardef linkHVH(text iLink)(expr pA, intX, pB)(expr texHead, texTail)=
   path thePath;
   thePath = pA -- (intX, ypart(pA)) -- (intX, ypart(pB)) -- pB;

   pathItem(iLink)(thePath)(texHead, texTail);
enddef;

% begin figure 1
beginfig(1);
Class.clplf("Platform")()();
Class.cldevid("DeviceID")()();
Class.clprogram("Program")()();
Class.clkernel("Kernel")()();
Class.clcmdq("CommanmdQueue")()();
Class.clcontext("Context")()();

Class.clmemobj("MemObject")()();
classStereotypes.clmemobj("<<abstract>>");

Class.clbuffer("Buffer")()();
Class.climg("Image")()();
Class.clevt("Event")()();
Class.clsampler("Sampler")()();

% layout
topToBottom(45)(clplf, cldevid);
topToBottom(30)(cldevid, clprogram);
topToBottom(30)(clprogram, clkernel);

leftToRight(60)(cldevid, clcontext);
clcmdq.se = clcontext.ne + (-10, 20);
leftToRight(30)(clcmdq, clevt);

topToBottom(30)(clcontext, clmemobj);
clbuffer.ne = clmemobj.s - (20, 30);
leftToRight(30)(clbuffer, climg);

leftToRight(20)(clmemobj, clsampler);

% draw objects
drawObjects(clplf, cldevid, clprogram, clkernel,
   clcontext, clcmdq, clevt, clmemobj, clbuffer, climg, clsampler);


linkV(associationUni)(1/3[cldevid.nw, cldevid.ne], clplf.bottom)("*", "1");

linkV(associationUni)(clprogram.n, cldevid.bottom)("*", "*");

linkV(composition)(clkernel.n, clprogram.bottom)("*", "1");

linkH(associationUni)(objEdgeLeft(clcontext, 1/5), cldevid.right)("*", "1..*");

linkHV(associationUni)(clcmdq.w, objEdgeTop(cldevid, 2/3))("*", "1");

linkH(composition)(clevt.w, clcmdq.right)("*", "0..1");

linkVHV(composition)(clcmdq.s, (clcmdq.bottom - 5),
   objEdgeTop(clcontext, 1/4))("*", "1");

linkVHV(composition)(clevt.s, (clevt.bottom - 5),
   objEdgeTop(clcontext, 3/4))("*", "0..1");

linkHVH(composition)(clprogram.e, (clprogram.right + 20),
   objEdgeLeft(clcontext, 4/5))("*", "1");

linkV(composition)(clmemobj.n, clcontext.bottom)("*", "1");

linkVHV(inheritance)(clbuffer.n, (clmemobj.bottom - 20), clmemobj.s)("", "");

linkVHV(inheritance)(climg.n, (clmemobj.bottom - 20), clmemobj.s)("", "");

linkVH(composition)(clsampler.n, objEdgeRight(clcontext, 4/5))("*", "1");

linkHVH(association)(objEdgeRight(clcontext, 1/5), clsampler.right, clplf.e)
   ("", "");

endfig;


end;

