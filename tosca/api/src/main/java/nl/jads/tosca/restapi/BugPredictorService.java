package nl.jads.tosca.restapi;

import kb.repository.KB;
import nl.jads.tosca.DefectPredictorKBApi;
import nl.jads.tosca.dto.BugRecord;
import nl.jads.tosca.dto.BugReport;
import nl.jads.tosca.dto.FindBugInput;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import javax.servlet.ServletContext;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

@Path("/bugs")
//@Api()
public class BugPredictorService {
    @Context
    ServletContext servletContext;

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
//    @ApiOperation(
//            value = "Returns the bugs in the IaC codes",
////			response = String.class,
//            responseContainer = "List")
    @Path("/tosca/jsonv2")
    public Response findBugsV2(FindBugInput findBugInput) throws IOException {
        String actualPath = servletContext.getRealPath("/WEB-INF/classes");

        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(getKB(findBugInput), actualPath);
        BugReport bugReport = kbApi.findBugs(findBugInput);
        IDEInput ideInput = new IDEInput();
        List<Warning> warningList = new ArrayList<>();
        for (BugRecord record : bugReport.getBugs()) {
            Warning warning = new Warning();
            warning.setType(record.getBugName());
            Info info = new Info();
            info.setContext(record.getContext());
            info.setName(record.getElementName());
            info.setElementType(record.getElementType());
            info.setDescription(record.getDescription());
            warning.setInfo(info);
            warning.setType(record.getBugName());
            warningList.add(warning);
        }
        ideInput.setWarnings(warningList);
        kbApi.shutDown();
        return Response.ok(ideInput).header(
                "Access-Control-Allow-Origin", "*").header("Access-Control-Allow-Origin", "POST").build();
    }

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
//    @ApiOperation(
//            value = "Returns the bugs in the IaC codes",
////			response = String.class,
//            responseContainer = "List")
    @Path("/tosca/json")
    public Response findBugs(FindBugInput findBugInput) throws IOException {
        String actualPath = servletContext.getRealPath("/WEB-INF/classes");
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(getKB(findBugInput), actualPath);
        BugReport bugReport = kbApi.findBugs(findBugInput);
        kbApi.shutDown();
        return Response.ok(bugReport).header("Access-Control-Allow-Origin", "*").header("Access-Control-Allow-Origin", "POST").build();
    }

    @POST
    @Path("/tosca/file")
    @Consumes(MediaType.MULTIPART_FORM_DATA)
    @Produces(MediaType.APPLICATION_JSON)
    public Response uploadFile(
            @FormDataParam("file") InputStream uploadedInputStream,
            @FormDataParam("file") FormDataContentDisposition fileDetail) throws IOException {
        String fileLocation = "e://" + fileDetail.getFileName();
        String actualPath = servletContext.getRealPath("/WEB-INF/classes");
        System.out.println("Received a File :" + fileLocation);
        //saving file
//        try {
//            FileOutputStream out = new FileOutputStream(new File(fileLocation));
//            int read = 0;
//            byte[] bytes = new byte[1024];
//            out = new FileOutputStream(new File(fileLocation));
//            while ((read = uploadedInputStream.read(bytes)) != -1) {
//                out.write(bytes, 0, read);
//            }
//            out.flush();
//            out.close();
//        } catch (IOException e) {e.printStackTrace();}
        FindBugInput findBugInput = new FindBugInput();
        findBugInput.setActionId(fileDetail.getFileName());
        findBugInput.setDeploymentId(fileDetail.getFileName());
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(new KB(), actualPath);
        BugReport bugReport = kbApi.findBugs(findBugInput);
        kbApi.shutDown();
        return Response.ok(bugReport).header("Access-Control-Allow-Origin", "*").header("Access-Control-Allow-Origin", "POST").build();
    }

    private KB getKB(FindBugInput findBugInput) {
        String server = findBugInput.getServer();
        if (server == null || "".equals(server.trim())) {
            server = KB.SERVER_URL;
        }
        String repo = findBugInput.getRepository();
        if (repo == null || "".equals(repo.trim())) {
            repo = KB.REPOSITORY;
        }
        return new KB(server, repo);
    }
}
